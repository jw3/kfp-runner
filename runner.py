import configargparse as argparse
import kfp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_name", type=str, help="Name for job")
    parser.add_argument("-e", "--experiment", type=str, default='testing', help="Experiment name")
    parser.add_argument("-p", "--pipeline", type=str, required=True, env_var='KF_PIPELINE_ID', help="Pipeline ID")
    args = parser.parse_args()

    client = kfp.Client()
    eid = client.get_experiment(experiment_name=args.experiment)

    if not eid:
        eid = client.create_experiment(args.experiment)

    client.run_pipeline(eid, args.job_name, pipeline_id=args.pipeline)
