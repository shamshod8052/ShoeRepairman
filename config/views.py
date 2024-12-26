from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from Product.models import Order, Work


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    work = order.last_work
    is_users_before_work = order.one_before_last_work
    if is_users_before_work:
        is_users_before_work = is_users_before_work.user == request.user
    context = {
        'user': request.user,
        'order': order,
        'work': work,
        'work_status': work.status if work else Work.Status.NOT_RECEIVED,
        'is_users_work': work.user == request.user if work else False,
        'is_users_before_work': is_users_before_work,
    }

    return render(request, 'order_detail.html', context=context)


@login_required
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    work = order.last_work
    if not work or work.status == Work.Status.REJECTED:
        order.works.create(user=request.user, status=Work.Status.IN_PROCESS)
    elif work.status == Work.Status.NOT_RECEIVED:
        if work.user == request.user:
            work.status = Work.Status.IN_PROCESS
            work.save(update_fields=['status'])
        else:
            order.works.create(user=request.user, status=Work.Status.IN_PROCESS)

    return redirect('order_detail', order_id = order_id)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    work = order.last_work
    if work and work.user == request.user and work.status == Work.Status.IN_PROCESS:
        work.status = Work.Status.NOT_RECEIVED
        work.save(update_fields=['status'])

    return redirect('order_detail', order_id = order_id)


@login_required
def success_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    work = order.last_work
    if work and work.user == request.user and work.status == Work.Status.IN_PROCESS:
        order.works.create(user=request.user, status=Work.Status.DONE)

    return redirect('order_detail', order_id = order_id)


@login_required
def approve_work(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    work = order.last_work
    is_admin = order.request_order.request.manager.is_admin
    is_manager = order.request_order.request.manager.is_manager
    if work and (is_admin or is_manager) and work.status == Work.Status.DONE:
        order.works.create(
            user=request.user,
            status=Work.Status.APPROVED,
            for_user_id=work.user.id
        )

    return redirect('order_detail', order_id = order_id)


@login_required
def reject_work(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    work = order.last_work
    is_admin = order.request_order.request.manager.is_admin
    is_manager = order.request_order.request.manager.is_manager
    if work and (is_admin or is_manager) and work.status == Work.Status.DONE:
        order.works.create(
            user=request.user,
            status=Work.Status.REJECTED,
            for_user_id=work.user.id
        )

    return redirect('order_detail', order_id=order_id)
