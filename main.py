from sensor.pipelines.training_pipeline import start_training_pipeline
if  __name__ == '__main__':
     try:
          start_training_pipeline()
     except Exception as e:
          print(e)