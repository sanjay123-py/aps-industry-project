from sensor.pipelines.training_pipeline import start_training_pipeline
from sensor.pipelines.batch_prediction import start_batch_prediction

if  __name__ == '__main__':
     try:
          # start_training_pipeline()
          output_file = start_batch_prediction('/config/workspace/aps_failure_training_set1.csv')
          print(output_file)
     except Exception as e:
          print(e)