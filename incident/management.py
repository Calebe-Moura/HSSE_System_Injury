def can_manage_injury(user, injury):

    return (
        user.is_superuser or
        injury.reported_by == user or
        injury.responsible == user
    )


def can_manage_action(user, injury):

    return (
        user.is_superuser
        or injury.reported_by == user
        or injury.responsible == user
    )