from .models import CandidateStatusHistory


def record_status_change(application, user, old_status, new_status, note=''):
    if old_status == new_status:
        return None
    return CandidateStatusHistory.objects.create(
        application=application,
        old_status=old_status or '',
        new_status=new_status,
        changed_by=user,
        note=note,
    )