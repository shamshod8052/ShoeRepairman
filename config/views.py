from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from Product.models import Order, Work


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    works = order.works.order_by('-status')
    work = works.first() if works.exists() else None
    work_status = work.status if work else None
    is_admin = request.user.groups.filter(name__in=['Admin']).exists
    is_manager = request.user.groups.filter(name__in=['Manager']).exists

    context = {
        'order': order, 'work': work, 'work_status': work_status,
        'is_admin': is_admin, 'is_manager': is_manager, 'user': request.user,
    }

    return render(request, 'order_detail.html', context=context)


@login_required
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    work, created = order.works.get_or_create(worker=request.user)
    work.status = Work.Status.RECEIVED
    work.save(update_fields=['status'])

    return redirect('order_detail', order_id = order_id)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        work = order.works.get(worker=request.user, status=Work.Status.RECEIVED)
        work.status = Work.Status.NOT_RECEIVED
        work.save(update_fields=['status'])
    except Work.DoesNotExist:
        ...

    return redirect('order_detail', order_id = order_id)


@login_required
def success_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        work = order.works.get(worker=request.user, status=Work.Status.RECEIVED)
        work.status = Work.Status.UNAPPROVED
        work.save(update_fields=['status'])
    except Work.DoesNotExist:
        ...

    return redirect('order_detail', order_id = order_id)


@login_required
def approve_work(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        work = order.works.get(status=Work.Status.UNAPPROVED)
        work.status = Work.Status.APPROVED
        work.save(update_fields=['status'])
    except Work.DoesNotExist:
        ...

    return redirect('order_detail', order_id = order_id)
