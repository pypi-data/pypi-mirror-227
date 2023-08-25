import json

from ...main import AppObject, Attribute
from ...relationships import many_to_many
from ..config import NameConfig
from .base import (
    AbstractModuleCode,
    SimpleDecoratorCode,
    SimpleFunctionCode,
    SimpleVariable,
)

pytest_dec = SimpleDecoratorCode(
    name='pytest.fixture',
)


class ConfTestModuleCode(AbstractModuleCode):
    def __init__(self, app_objs: list[AppObject], config: NameConfig):
        self.type_checking_imports = {}
        self.classes = []
        self.functions = [self.get_client_function()]
        self.variables = []
        self.config = config
        self.folder = ''
        self.filename = 'conftest'
        self.imports = {
            'pytest': set(),
            'sqlalchemy': {'create_engine'},
            'sqlalchemy.orm': {'sessionmaker'},
            'sqlalchemy.pool': {'StaticPool'},
            'fastapi.testclient': {'TestClient'},
            f'{config.app_foldername}.{config.base_file}': {'Base'},
            f'{config.app_foldername}.{config.dependency_file}': {'get_db'},
            f'{config.app_foldername}.main': {'app'},
        }
        self.create_fixtures(app_objs)

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.functions_code}
""".strip(
            '\n'
        )

    def get_client_function(self) -> SimpleFunctionCode:
        content = """
TEST_DB = "sqlite://"
engine = create_engine(
    TEST_DB,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
with TestClient(app) as c:
    yield c
"""
        f = SimpleFunctionCode(
            name='client',
            content=content,
            decorators=[pytest_dec],
        )
        return f

    def create_fixtures(self, app_objs: list[AppObject]) -> None:
        for app_obj in app_objs:
            content = self.get_test_data(app_obj)
            f = SimpleFunctionCode(
                name=f'get_{app_obj.name}',
                return_value='dict[str,str]',
                content=f'return {content}',
                decorators=[pytest_dec],
            )
            self.functions.append(f)

    def get_test_data(self, app_obj: AppObject) -> str:
        content_dict = {}
        for att in app_obj.attributes:
            content_dict[att.name] = get_att_data(att)
        for rel in app_obj.all_relationships:
            if not app_obj.is_relationship_many(rel):
                name = f'{app_obj.get_rel_name(rel)}_id'
                content_dict[name] = '1'
        return json.dumps(content_dict)


class TestModuleCode(AbstractModuleCode):
    def __init__(self, app_objs: list[AppObject], config: NameConfig):
        self.type_checking_imports = {}
        self.classes = []
        self.functions = []
        self.variables = []
        self.config = config
        self.folder = ''
        self.filename = 'test_route'
        self.imports = {
            'pytest': set(),
            'fastapi.testclient': {'TestClient'},
        }
        self.create_tests(app_objs)

    def __str__(self) -> str:
        return f"""
{self.imports_code}
{self.functions_code}
""".strip(
            '\n'
        )

    def create_tests(self, app_objs: list[AppObject]) -> None:
        for app_obj in app_objs:
            params, cont = self.get_test_data(app_obj)
            f = SimpleFunctionCode(
                name=f'test_{app_obj.name}',
                parametars=list(params),
                content=cont,
            )
            self.functions.append(f)

    def get_test_data(self, app_obj: AppObject) -> tuple[list[SimpleVariable], str]:
        params = [
            SimpleVariable('client', 'TestClient'),
            SimpleVariable(f'get_{app_obj.name}', 'dict[str,str]'),
        ]
        init_creation: dict[str, str] = {}
        assert_att: list[str] = []
        order: dict[str, int] = {}
        skip_param = app_obj.name
        for att in app_obj.attributes:
            res = get_att_data(att)
            if not isinstance(res, int):
                res = f"'{res}'"
            assert_att.append(f"assert data['{att.name}'] == {res}")
        for rel in app_obj.all_relationships:
            rel_name = app_obj.get_rel_name(rel)
            rel_obj = app_obj.get_rel_obj(rel)
            if app_obj.is_relationship_many(rel):
                # assert_att.append(f"assert data['{rel_name}_id'] == [1]")
                if rel.relationship_type == many_to_many:
                    check_creation(rel_obj, init_creation, order, 1, params, skip_param)
            else:
                check_creation(rel_obj, init_creation, order, 1, params, skip_param)
                assert_att.append(f"assert data['{rel_name}_id'] == 1")
        sorted_order = dict(sorted(order.items(), key=lambda x: x[1], reverse=True))
        assert_att_code = '\n'.join(assert_att)
        creation_code_list: list[str] = []
        for key in sorted_order.keys():
            creation_code_list.append(init_creation[key])

        init_creation_code = '\n'.join(creation_code_list)
        content = f"""
{init_creation_code}

response = client.post('/api/v1/{app_obj.route_name}',json=get_{app_obj.name})
assert response.status_code == 201, response.text
data = response.json()
assert "id" in data
id = data["id"]
{assert_att_code}

response = client.get(f"/api/v1/{app_obj.route_name}/{{id}}")
assert response.status_code == 200, response.text
data = response.json()
assert data["id"] == id
{assert_att_code}

response = client.delete(f"/api/v1/{app_obj.route_name}/{{id}}")
assert response.status_code == 200, response.text
data = response.json()
assert data["message"] == "Resource successfully deleted."

response = client.get(f"/api/v1/{app_obj.route_name}/{{id}}")
assert response.status_code == 404, response.text
data = response.json()
assert data["detail"] == f"{app_obj.class_name} with ID {{id}} not found!"
"""
        return params, content


def check_creation(
    obj: AppObject,
    init_creation: dict[str, str],
    order: dict[str, int],
    order_num: int,
    params: list[SimpleVariable],
    skip_param: str,
) -> None:
    name = obj.name
    if not init_creation.get(name) and name != skip_param:
        init_creation[name] = f"client.post('/api/v1/{obj.route_name}',json=get_{name})"
        params.append(SimpleVariable(f'get_{name}', 'dict[str,str]'))
        order[name] = order_num
        order_num += 1
        for rel in obj.all_relationships:
            to_create: bool = rel.relationship_type == many_to_many or not obj.is_relationship_many(rel)
            if to_create:
                new_obj = obj.get_rel_obj(rel)
                check_creation(new_obj, init_creation, order, order_num, params, skip_param)


# TODO: this should be change to get data from faker library
def get_att_data(att: Attribute) -> str | int:
    if att.type.python_type == 'str':
        return att.name
    if att.type.python_type == 'int':
        return 1
    if att.type.python_type == 'date':
        return '2020-11-20'
    if att.type.python_type == 'time':
        return '07:44'
    return 'test'  # pragma: no cover
