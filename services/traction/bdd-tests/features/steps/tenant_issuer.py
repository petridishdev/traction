import json, random, string
import requests
import time
from behave import *
from starlette import status


@given('"{tenant}" registers as an issuer')
@when('"{tenant}" registers as an issuer')
def step_impl(context, tenant: str):
    response = requests.post(
        context.config.userdata.get("traction_host") + "/tenant/v1/admin/make-issuer",
        headers=context.config.userdata[tenant]["auth_headers"],
    )
    assert response.status_code == status.HTTP_200_OK, response.__dict__
    resp_json = json.loads(response.content)
    # wait for endorser signatures and ledger writes
    time.sleep(20)


@when('"{issuer}" issues "{holder}" a "{schema_name}" credential')
def step_impl(context, issuer: str, holder: str, schema_name: str):

    schema_template = context.config.userdata[issuer]["schema_template"]
    credential_template = context.config.userdata[issuer]["credential_template"]
    contact_id = context.config.userdata[issuer]["connections"][holder]["contact_id"]

    schema_attrs = schema_template["attributes"]
    credential_template_id = credential_template["credential_template_id"]
    data = {
        "contact_id": contact_id,
        "credential_template_id": credential_template_id,
        "attributes": [
            {
                "name": attr_name,
                "value": "".join(random.choice(string.ascii_letters)),
            }
            for attr_name in schema_attrs
        ],
    }

    response = requests.post(
        context.config.userdata.get("traction_host") + "/tenant/v1/issuer/credentials",
        headers=context.config.userdata[issuer]["auth_headers"],
        json=data,
    )
    assert response.status_code == status.HTTP_200_OK, response.__dict__


@then('"{issuer}" will have an acked credential_offer')
def step_impl(context, issuer):
    response = requests.get(
        context.config.userdata.get("traction_host")
        + "/tenant/v1/issuer/credentials"
        + "?status=Issued",
        headers=context.config.userdata[issuer]["auth_headers"],
    )
    assert response.status_code == status.HTTP_200_OK, response.status
    resp_json = json.loads(response.content)
    assert len(resp_json["items"]) == 1, resp_json


## COMPOSED ACTIONS
@given('"{tenant}" is an issuer')
def step_impl(context, tenant):
    context.execute_steps(
        f"""
    Given "{tenant}" is allowed to be an issuer by the innkeeper
    And "{tenant}" registers as an issuer
    And we sadly wait for {5} seconds because we have not figured out how to listen for events
    And "{tenant}" will have a public did   
    """
    )