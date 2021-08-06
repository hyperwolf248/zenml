from abc import abstractmethod

from tfx.orchestration import metadata
from tfx.orchestration import pipeline as tfx_pipeline
from tfx.orchestration.local.local_dag_runner import LocalDagRunner

from playground.datasources.base_datasource import BaseDatasource
from playground.steps.base_step import BaseStep
from playground.utils.annotations import GenericType
from playground.utils.exceptions import PipelineInterfaceError

Datasource = type("Datasource",
                  (GenericType,),
                  {"VALID_TYPES": [BaseDatasource]})

Step = type("Step",
            (GenericType,),
            {"VALID_TYPES": [BaseStep]})


class BasePipeline:
    STEP_SPEC = None
    DATASOURCE_SPEC = None

    def __init__(self, *args, **kwargs):
        self.__steps = dict()
        self.__datasources = dict()

        if args:
            raise PipelineInterfaceError("")  # TODO: Fill

        for k, v in kwargs.items():
            assert k in self.STEP_SPEC or k in self.DATASOURCE_SPEC

            if k in self.STEP_SPEC:
                self.__steps.update({k: v})  # TODO: assert class
            elif k in self.DATASOURCE_SPEC:
                self.__datasources.update({k: v})
            else:
                raise PipelineInterfaceError("")  # TODO: Fill

    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    def run(self):
        from tfx.dsl.components.common.importer import Importer
        from playground.artifacts.data_artifacts import CSVArtifact

        data = Importer(
            source_uri="/home/baris/Maiot/zenml/local_test/data",
            artifact_type=CSVArtifact).with_id("datasource")

        self.connect(datasource=data.outputs.result, **self.__steps)

        step_list = [data] + \
                    [s.get_component() for s in self.__steps.values()]

        created_pipeline = tfx_pipeline.Pipeline(
            pipeline_name='pipeline_name',
            pipeline_root='/home/baris/Maiot/zenml/local_test/new_zenml/',
            components=step_list,
            enable_cache=False,
            metadata_connection_config=metadata.sqlite_metadata_connection_config(
                '/home/baris/Maiot/zenml/local_test/new_zenml/db'),
            beam_pipeline_args=[
                '--direct_running_mode=multi_processing',
                '--direct_num_workers=0'])

        LocalDagRunner().run(created_pipeline)
