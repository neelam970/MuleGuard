from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    return user_passes_test(
        lambda user: user.groups.filter(name="Admin").exists()
    )(view_func)


def analyst_required(view_func):
    return user_passes_test(
        lambda user: user.groups.filter(name="AML Analyst").exists()
    )(view_func)


def investigator_required(view_func):
    return user_passes_test(
        lambda user: user.groups.filter(name="Investigator").exists()
    )(view_func)