import json
import boto3
from neuralpit.utils.paramstore import appSettings

firehouse = boto3.client('firehouse',region_name='ap-southeast-2')

class NeuralPitUsageTracker:

    def __init__(self, stream):
        self._stream = stream

    def trackUsage(self,record):
        firehouse.put_record(
            DeliveryStreamName=self._stream,
            Record={
                'Data': json.dumps(record)
            }
        )
usageTracker = NeuralPitUsageTracker(appSettings.get('OPENAI_TRACKER_STREAM'))