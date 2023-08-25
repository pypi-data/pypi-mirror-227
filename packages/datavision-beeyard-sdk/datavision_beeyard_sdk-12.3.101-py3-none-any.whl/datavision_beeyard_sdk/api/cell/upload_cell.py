from ...client import AuthenticatedClient
from ...models.tag_dto import TagDto
from ...models.property_dto import PropertyDto
from ...models.upload_cell_multipart_data import UploadCellMultipartData


def upload(
    *,
    client: AuthenticatedClient,
    files: UploadCellMultipartData,
    tags: [TagDto],
    properties: [PropertyDto],
):
    """Upload cell to BeeYard.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    files : UploadCellMultipartData
        Object containing list of files containing cells to be uploaded.
    tags : list[TagDto]
        List of cell tags.
    properties : list[PropertyDto]
        List of cell properties.

    Returns
    -------
    Response
        Http response from API.
    """
    url = "{}/api/v1/cells?".format(client.base_url)
    tag_dict = [i.to_dict() for i in tags]
    props_dict = [i.to_dict() for i in properties]
    for t in tag_dict:
        url = url + t.category + "=" + t.name + "&"
    for p in props_dict:
        url = url + p.key + "=" + p.value + "&"
    url = url[:-1]
    file_list = files.to_dict()
    response = client.post(url, headers=client.token_headers, files=file_list)
    return response
