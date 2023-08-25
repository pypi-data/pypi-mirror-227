from eolymp.atlas import statement_pb2, library_service_pb2, statement_service_pb2, testing_service_pb2
from eolymp.atlas.atlas_http import AtlasClient
from eolymp.ecm import content_pb2

from peolymp.abstract import AbstractAPI
from peolymp.utils import get_many


class AtlasAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(AtlasAPI, self).__init__(**kwargs)
        self.client = AtlasClient(self.http_client, url=self.get_url())

    def create_statement(self, prob_id, locale, title, link, source=""):
        s = statement_pb2.Statement(problem_id=prob_id, locale=locale, title=title,
                                    content=content_pb2.Content(latex=" "), download_link=link, source=source)
        return self.client.CreateStatement(statement_service_pb2.CreateStatementInput(problem_id=prob_id,
                                                                                      statement=s)).statement_id

    def update_statement(self, problem_id, statement):
        return self.client.UpdateStatement(
            statement_service_pb2.UpdateStatementInput(problem_id=problem_id, statement_id=statement.id,
                                                       statement=statement))

    def delete_statement(self, prob_id, statement_id):
        self.client.DeleteStatement(statement_service_pb2.DeleteStatementInput(statement_id=statement_id,
                                                                               problem_id=prob_id))

    def get_statements(self, prob_id):
        return self.client.ListStatements(statement_service_pb2.ListStatementsInput(problem_id=prob_id)).items

    def get_problems(self):
        def __get_problems(offset, size):
            return self.client.ListProblems(request=library_service_pb2.ListProblemsInput(offset=offset, size=size))

        return get_many(__get_problems)

    def delete_testset(self, problem_id, testset_id):
        return self.client.DeleteTestset(testing_service_pb2.DeleteTestsetInput(problem_id=problem_id,
                                                                                testset_id=testset_id))
