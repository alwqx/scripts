import logging

from kubernetes import watch
from kubernetes.client import Configuration, CoreV1Api, ApiClient

logger = logging.getLogger(__name__)


class EventHandler():

    def __init__(self, job_name, region_id, token, host, namespace='default', timeout=10):
        """Init
        :param task: event task
        :type task: event_task.models.EventTask
        """
        self.job_name = job_name
        self.region_id = region_id
        self.token = token
        self.host = host
        self.namespace = namespace
        self.timeout = timeout

    def run(self):
        self.process_build_events()

    def process_build_events(self):
        """
        Retrive k8s job events and save to log store(elasticsearch)
        This method is common for k8s
        """
        logger.info('start process k8s event...')
        print('start process k8s event...')
        pod_name = None
        pod_count, job_count = 0, 0
        msg_cache = []
        w = watch.Watch()

        config = Configuration()
        config.verify_ssl = False
        config.api_key_prefix = {'authorization': 'Bearer'}
        config.api_key = {'authorization': self.token}
        config.host = self.host
        pod_client = CoreV1Api(api_client=ApiClient(configuration=config))

        logger.info('start handle events for job {}'.format(self.job_name))
        for event in w.stream(pod_client.list_namespaced_event,
                              timeout_seconds=self.timeout,
                              namespace=self.namespace):
            raw_event = event['raw_object']
            if raw_event['involvedObject']['name'] == self.job_name:
                if not pod_name and 'Created pod:' in raw_event['message']:
                    pod_name = self._get_pod_name(raw_event['message'])

                if raw_event['message'] not in msg_cache:
                    msg_cache.append(raw_event['message'])
                    msg = self._gen_event_msg(raw_event)
                    logger.info(msg)
                    job_count += 1

            if raw_event['involvedObject']['name'] == pod_name:
                if raw_event['message'] not in msg_cache:
                    msg_cache.append(raw_event['message'])
                    msg = self._gen_event_msg(raw_event)
                    logger.info(msg)
                    pod_count += 1

        logger.info('get {} event for job {} within {}s'.format(job_count,
                                                                self.job_name,
                                                                self.timeout))
        if pod_name:
            logger.info('get {} event for pod {} within {}s'.format(pod_count,
                                                                    pod_name,
                                                                    self.timeout))
        logger.info('handle events for job {} done'.format(self.job_name))
        print('process k8s event done')

    def _get_pod_name(self, message):
        name = message[len('Created pod:'):]
        return str.strip(name)

    def _gen_event_msg(self, event):
        """
        Generate event message

        :param event: event from k8s event(raw object)
        :type event: dict
        :returns: message
        :rtype: str
        """

        msg = '[{}][{}][{}] > {}'.format(str.title(event['source']['component']),
                                         event['involvedObject']['kind'],
                                         event['reason'],
                                         event['message'])
        return msg

def get_pod_client():
    config = Configuration()
    token = 'k8s_token'
    host = 'k8s_host'
    config.verify_ssl = False
    config.api_key_prefix = {'authorization': 'Bearer'}
    config.api_key = {'authorization': token}
    config.host = host

    # return CoreV1Api(api_client=ApiClient(configuration=config))
    return CoreV1Api(api_client=ApiClient(config=config))

def gen_event_msg(event):
    """
    Generate event message

    :param event: event from k8s event(raw object)
    :type event: dict
    :returns: message
    :rtype: str
    """

    msg = '[{}][{}][{}][{}] > {}'.format(str.title(event['source']['component']),
                                     event['involvedObject']['kind'],
                                     event['reason'],
                                     event['involvedObject']['name'],
                                     event['message'])
    return msg

def stream_event():
    timeout = 12000
    print('start process k8s event...')
    count = 0
    w = watch.Watch()
    pod_client = get_pod_client()

    for event in w.stream(pod_client.list_namespaced_event,
                          timeout_seconds=timeout,
                          namespace='default'):
        raw_event = event['raw_object']
        msg = gen_event_msg(raw_event)
        logger.info(msg)
        print(msg)
        count += 1

    logger.info('get {} events within {}s'.format(count, timeout))
    print('get {} events within {}s'.format(count, timeout))
    print('process k8s event done')

"""
[Job-Controller][Job][SuccessfulCreate][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b] > Created pod: private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w
[Default-Scheduler][Pod][Scheduled][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > Successfully assigned private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w to 10.24.0.6
[Kubelet][Pod][SuccessfulMountVolume][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > MountVolume.SetUp succeeded for volume "1"
[Kubelet][Pod][SuccessfulMountVolume][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > MountVolume.SetUp succeeded for volume "2"
[Kubelet][Pod][SuccessfulMountVolume][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > MountVolume.SetUp succeeded for volume "0"
[Kubelet][Pod][SuccessfulMountVolume][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > MountVolume.SetUp succeeded for volume "default-token-mwlfz"
[Kubelet][Pod][Pulling][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > pulling image "index.alauda.cn/alaudaorg/rattletrap:6926063c7fc1d318f32dae719968ecd078ba6655"
[Kubelet][Pod][Pulled][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > Successfully pulled image "index.alauda.cn/alaudaorg/rattletrap:6926063c7fc1d318f32dae719968ecd078ba6655"
[Kubelet][Pod][Created][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > Created container
[Kubelet][Pod][Started][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > Started container
[Kubelet][Pod][Killing][private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b-87k3w] > Killing container with id docker://private-build-0c04f853-a651-42a6-a4ab-bd82cac6718b:Need to kill Pod

import event_debug
event_debug.stream_event()
"""
