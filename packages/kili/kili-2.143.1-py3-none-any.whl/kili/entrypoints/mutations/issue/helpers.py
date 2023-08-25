"""Helpers for the issue mutations."""


from typing import List, Literal, cast

from kili.core.graphql import QueryOptions
from kili.core.graphql.operations.issue.queries import IssueQuery, IssueWhere
from kili.core.graphql.operations.label.queries import LabelQuery, LabelWhere
from kili.exceptions import NotFound


# pylint: disable=missing-type-doc
def get_issue_numbers(kili, project_id: str, type_: Literal["QUESTION", "ISSUE"], size: int):
    """Get the next available issue number.

    Args:
        kili: Kili instance.
        project_id: Id of the project.
        type_: type of the issue to add.
        size: the number of issue to add.
    """
    issues = IssueQuery(kili.graphql_client, kili.http_client)(
        IssueWhere(
            project_id=project_id,
        ),
        ["type", "issueNumber"],
        QueryOptions(disable_tqdm=True),
    )
    first_issue_number = (
        cast(
            int,
            max(
                (issue["issueNumber"] for issue in issues if issue["type"] == type_),
                default=-1,
            ),
        )
        + 1
    )

    return list(range(first_issue_number, first_issue_number + size))


def get_labels_asset_ids_map(kili, project_id: str, label_id_array: List[str]):
    """Return a dictionary that gives for every label id, its associated asset id.

    Returns:
        a dict of key->value: a label id->its associated asset id for the given label ids
    Raises:
        NotFound error if at least one label was not found with its given id
    """
    options = QueryOptions(disable_tqdm=True)
    where = LabelWhere(
        project_id=project_id,
        id_contains=label_id_array,
    )
    labels = list(
        LabelQuery(kili.graphql_client, kili.http_client)(
            where=where, fields=["labelOf.id", "id"], options=options
        )
    )
    labels_not_found = [
        label_id for label_id in label_id_array if label_id not in [label["id"] for label in labels]
    ]
    if len(labels_not_found) > 0:
        raise NotFound(str(labels_not_found))
    return {label["id"]: label["labelOf"]["id"] for label in labels}
