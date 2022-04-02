from ..model.create_database import User
from ..model.create_database import Gifts, Order, OrderItems, Size
from ..model.create_database import Wishlist, WishlistItems
from flask import make_response, jsonify
from ..connect_to_aws import database
import random
import string
import datetime

def create_wishlist(info):
    response_data = {
        "message": "success",
        "owner_id": "none",
        "wishlist_id": "none"
    }
    owner_id = info['owner_id']
    check_length = Wishlist.query.filter_by(owner_id=owner_id).all()
    check_user = User.query.filter_by(id=owner_id).first()
    if not check_user:
        status_code = 404
        response_data['message'] = 'User does not exist.'
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if len(check_length) >= 5:
        status_code = 400
        response_data['message'] = 'Each user can have no more than 5 wishlists.'
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    owner_first_name = info['owner_first_name']
    owner_last_name = info['owner_last_name']
    wishlist_name = info['wishlist_name']
    description = info['description']
    address = info['address']
    phone = info['phone']
    postcode = info['postcode']
    wishlist_id = ''.join(random.sample(string.ascii_letters + string.digits, 17))
    new_wishlist = Wishlist(wishlist_id=wishlist_id, owner_id=owner_id, wishlist_name=wishlist_name,
                                      wishlist_description=description, first_name=owner_first_name,
                            last_name=owner_last_name, address=address, phone=phone, postcode=postcode
                            )
    database.session.add(new_wishlist)
    database.session.commit()
    status_code = 200
    response_data['wishlist_id'] = wishlist_id
    response_data['owner_id'] = owner_id
    resp = make_response(response_data)
    resp.status_code = status_code
    database.session.close()
    return resp


def delete_wishlist(info):
    response_data = {
        "message": "success",
        "owner_id": "none",
        "wishlist_id": "none"
    }
    owner_id = info['owner_id']
    wishlist_id = info['wishlist_id']
    check_auth = Wishlist.query.filter_by(wishlist_id=wishlist_id).first()
    if not check_auth:
        status_code = 404
        response_data['message'] = 'This wishlist does not exist.'
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if int(owner_id) != int(check_auth.owner_id):
        status_code = 400
        response_data['message'] = 'A wishlist can only be deleted by its owner.'
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    Wishlist.query.filter_by(wishlist_id=wishlist_id).delete()
    WishlistItems.query.filter_by(products_id=wishlist_id).delete()
    database.session.commit()
    status_code = 200
    response_data['wishlist_id'] = wishlist_id
    response_data['owner_id'] = owner_id
    resp = make_response(response_data)
    resp.status_code = status_code
    database.session.close()
    return resp


def add_items(info):
    response_data = {
        "message": "success",
        'owner_id': 'none',
        "product_id": "none",
        "wishlist_id": "none"
    }
    add_seccussfully = {
        "message": "success",
    }
    check_owner = Wishlist.query.filter_by(owner_id=info['owner_id']).first()
    check_product = Gifts.query.filter_by(id=info['product_id']).first()
    check_duplicate = WishlistItems.query.filter_by(wishlist_id=info['wishlist_id'], products_id=info['product_id']).first()
    check_size = WishlistItems.query.filter_by(wishlist_id=info['wishlist_id'], products_id=info['product_id'], size=info['size']).first()
    if not check_owner:
        response_data['message'] = 'This user has no wishlist.'
        status_code = 404
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if not check_product:
        response_data['message'] = 'This product does not exist.'
        response_data['owner_id'] = info['owner_id']
        status_code = 404
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if check_duplicate:
        if check_size:
            add_seccussfully['message'] = 'add one gift in this wishlist successfully.'
            status_code = 200
            resp = make_response(add_seccussfully)
            resp.status_code = status_code
            check_size.count = check_size.count + 1
            database.session.commit()
            database.session.close()
            return resp
        else:
            pass
    owner_id = info['owner_id']
    wishlist_id = info['wishlist_id']
    product_id = info['product_id']
    product_name = info['product_name']
    cover_url = info['cover_url']
    size = info['size']
    price = info['price']
    find_wishlistID = Wishlist.query.filter_by(wishlist_id=info['wishlist_id']).first()
    wishlistID = find_wishlistID.id
    product = WishlistItems(wishlist_id=wishlist_id, wishlistID = wishlistID,products_id=product_id, product_name=product_name, product_cover=cover_url,
                            size=size, price=price, count=1)
    database.session.add(product)
    database.session.commit()
    status_code = 200
    response_data['wishlist_id'] = wishlist_id
    response_data['owner_id'] = owner_id
    response_data['product_id'] = product_id
    resp = make_response(response_data)
    resp.status_code = status_code
    database.session.close()
    return resp


def remove_item(info):
    response_data = {
        "message": "success",
        'owner_id': 'none',
        "product_id": "none",
        "wishlist_id": "none"
    }
    check_owner = Wishlist.query.filter_by(owner_id=info['owner_id']).first()
    check_product = Gifts.query.filter_by(id=info['product_id']).first()
    check_exists = WishlistItems.query.filter_by(wishlist_id=info['wishlist_id'],
                                                    products_id=info['product_id']).first()
    if not check_owner:
        response_data['message'] = 'This user has no wishlist.'
        status_code = 404
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if not check_product:
        response_data['message'] = 'This product does not exist.'
        response_data['owner_id'] = info['owner_id']
        status_code = 404
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    if not check_exists:
        response_data['message'] = 'This product does not in this wishlist.'
        status_code = 400
        resp = make_response(response_data)
        resp.status_code = status_code
        database.session.close()
        return resp
    owner_id = info['owner_id']
    wishlist_id = info['wishlist_id']
    product_id = info['product_id']
    WishlistItems.query.filter_by(products_id=product_id, wishlist_id=wishlist_id).delete()
    database.session.commit()
    status_code = 200
    response_data['wishlist_id'] = wishlist_id
    response_data['owner_id'] = owner_id
    response_data['product_id'] = product_id
    resp = make_response(response_data)
    resp.status_code = status_code
    database.session.close()
    return resp


def show_all(info):
    status_code = 200
    wishlists = Wishlist.query.filter_by(owner_id=info['owner_id']).all()
    response_message = {
        "message": "success"
    }
    response_data = {
        "wishlists_inf": []
    }
    if not wishlists:
        response_message['message'] = 'This user has no wishlist.'
        status_code = 404
        resp = make_response(response_message)
        resp.status_code = status_code
        database.session.close()
        return resp
    l = []
    for o in wishlists:
        wishlists_inf = {
            "id": o.id,
            "wishlist_id": o.wishlist_id,
            "owner_id": o.owner_id,
            "wishlist_name": o.wishlist_name,
            "wishlist_description": o.wishlist_description,
            "first_name": o.first_name,
            "last_name": o.last_name,
            "address": o.address,
            "phone": o.phone,
            "postcode": o.postcode,
            "state": o.state,
            "payer_fname": o.payer_fname,
            "products": [],
        }
        productList = WishlistItems.query.filter_by(wishlist_id=o.wishlist_id).all()
        L = []
        # if not productList:
        #     continue
        for p in productList:
            p_list = {"products_id": p.products_id,
                      "product_name": p.product_name,
                      "product_cover": p.product_cover,
                      "size": p.size,
                      "price": p.price,
                      "count": p.count
                      }
            L.append(p_list)
        wishlists_inf["products"] = L
        l.append(wishlists_inf)
    response_data["wishlists_inf"] = l
    resp = make_response(response_message)
    resp.status_code = status_code
    resp.response_data = response_data
    database.session.close()
    return resp


def pay_wishlist(info):
    status_code = 200
    response_message = {
        "message": "success"
    }
    response_data = {
        "owner_id": '',
        "wishlist_id": '',
        "owner_first_name": '',
        "owner_last_name": '',
        "payer_first_name": '',
        "payer_id": 'null'
    }
    owner_id = info['owner_id']
    owner_first_name = info['owner_first_name']
    owner_last_name = info['owner_last_name']
    wishlist_id = info['wishlist_id']
    phone = info['phone']
    address = info['address']
    postcode = info['postcode']
    payer_first_name = info['payer_first_name']
    payer_id = info['payer_id']
    total_price = info['total_price']
    product_list = info['product_list']
    order_number = ''.join(random.sample(string.ascii_letters + string.digits, 15))
    check_owner = Wishlist.query.filter_by(owner_id=owner_id, wishlist_id=wishlist_id).first()
    check_payer = User.query.filter_by(id=payer_id).first()
    check_state = Wishlist.query.filter_by(wishlist_id=wishlist_id, state='completed').first()
    if not check_owner:
        status_code = 404
        response_message['message'] = 'This owner or wishlist does not exist.'
        resp = make_response(response_message)
        resp.status_code = status_code
        database.session.close()
        return resp
    if not check_payer:
        # status_code = 404
        # response_message['message'] = 'This payer does not exist.'
        # resp = make_response(response_message)
        # resp.status_code = status_code
        # return resp
        order_time = datetime.datetime.now()
        order = Order(order_time=order_time, order_total=total_price, order_number=order_number,
                      first_name=owner_first_name, last_name=owner_last_name, phone=phone,
                      address=address, postcode=postcode)
        # order = Order(user_id=payer_id, order_time=order_time, order_total=total_price, order_number=order_number,
        #               first_name=owner_first_name, last_name=owner_last_name, phone=phone,
        #               address=address, postcode=postcode)

        database.session.add(order)
        database.session.flush()
        database.session.refresh(order)
        oid = order.id
        for product in product_list:
            product_id = product['products_id']
            product_name = product['product_name']
            product_cover = product['product_cover']
            size = product['size']
            count = product['count']
            price = product['price']
            check_stock = Size.query.filter_by(gift_id=product_id, size=size).first()
            if not check_stock or check_stock.stock < 1:
                status_code = 400
                response_message['message'] = 'Product ' + str(product_id) + ' out of stock.'
                WishlistItems.query.filter_by(products_id=product_id, wishlist_id=wishlist_id).delete()
                database.session.commit()
                resp = make_response(response_message)
                resp.status_code = status_code
                database.session.close()
                return resp
            order_product = OrderItems(gift_name=product_name, item_cover_url=product_cover, size=size,
                                         count=count,
                                         price=price, each_total_price=price,
                                         productID=product_id, order_id=oid)
            database.session.add(order_product)
            each_size = Size.query.filter_by(gift_id=product_id, size=size).first()
            product_info = Gifts.query.filter_by(id=product_id).first()
            each_stock = each_size.stock
            each_sales = each_size.this_size_sales
            each_income = each_size.this_size_income
            each_size.stock = each_stock - 1
            each_size.this_size_sales = each_sales + 1
            each_size.this_size_income = each_income + price
            product_sales = product_info.gift_sales
            product_income = product_info.gift_income
            product_info.gift_sales = product_sales + 1
            product_info.gift_income = product_income + price
        update_wishlist = Wishlist.query.filter_by(owner_id=owner_id, wishlist_id=wishlist_id).first()
        update_wishlist.state = 'completed'
        update_wishlist.payer_fname = payer_first_name
        database.session.commit()
        response_data['owner_id'] = owner_id
        response_data['wishlist_id'] = wishlist_id
        response_data['owner_first_name'] = owner_first_name
        response_data['owner_last_name'] = owner_last_name
        response_data['payer_first_name'] = payer_first_name
        # response_data['payer_id'] = payer_id
        resp = make_response(response_message)
        resp.status_code = status_code
        resp.response_data = response_data
        database.session.close()
        return resp
    if check_state:
        status_code = 400
        response_message['message'] = 'This wishlist is already completed.'
        resp = make_response(response_message)
        resp.status_code = status_code
        return resp
    order_time = datetime.datetime.now()
    order = Order(user_id=payer_id, order_time=order_time, order_total=total_price, order_number=order_number,
                  first_name=owner_first_name, last_name=owner_last_name, phone=phone,
                  address=address, postcode=postcode)

    database.session.add(order)
    database.session.flush()
    database.session.refresh(order)
    oid = order.id
    for product in product_list:
        product_id = product['products_id']
        product_name = product['product_name']
        product_cover = product['product_cover']
        size = product['size']
        count = product['count']
        price = product['price']
        check_stock = Size.query.filter_by(gift_id=product_id, size=size).first()
        if not check_stock or check_stock.stock < 1:
            status_code = 400
            response_message['message'] = 'Product ' + str(product_id) + ' out of stock.'
            WishlistItems.query.filter_by(products_id=product_id, wishlist_id=wishlist_id).delete()
            database.session.commit()
            resp = make_response(response_message)
            resp.status_code = status_code
            database.session.close()
            return resp
        order_product = OrderItems(gift_name=product_name, item_cover_url=product_cover, size=size,
                                                  count=count,
                                                  price=price, each_total_price=price,
                                                  productID=product_id, order_id=oid)
        database.session.add(order_product)
        each_size = Size.query.filter_by(gift_id=product_id, size=size).first()
        product_info = Gifts.query.filter_by(id=product_id).first()
        each_stock = each_size.stock
        each_sales = each_size.this_size_sales
        each_income = each_size.this_size_income
        each_size.stock = each_stock - 1
        each_size.this_size_income = each_sales + 1
        each_size.individual_income = each_income + price
        product_sales = product_info.gift_sales
        product_income = product_info.gift_income
        product_info.gift_sales = product_sales + 1
        product_info.gift_income = product_income + price
    update_wishlist = Wishlist.query.filter_by(owner_id=owner_id, wishlist_id=wishlist_id).first()
    update_wishlist.state = 'completed'
    update_wishlist.payer_fname = payer_first_name
    database.session.commit()
    response_data['owner_id'] = owner_id
    response_data['wishlist_id'] = wishlist_id
    response_data['owner_first_name'] = owner_first_name
    response_data['owner_last_name'] = owner_last_name
    response_data['payer_first_name'] = payer_first_name
    response_data['payer_id'] = payer_id
    resp = make_response(response_message)
    resp.status_code = status_code
    resp.response_data = response_data
    database.session.close()
    return resp


def search(info):
    response_message = {
        "message": "success"
    }
    status_code = 200
    response_data = {
        "id": '',
        "wishlist_id": '',
        "owner_id": '',
        "wishlist_name": '',
        "wishlist_description": '',
        "first_name": '',
        "last_name": '',
        "address": '',
        "phone": '',
        "postcode": '',
        "state": '',
        "payer_fname": '',
        "products": [],
    }
    wishlist_id = info['wishlist_id']
    check_valid = Wishlist.query.filter_by(wishlist_id=wishlist_id).first()
    if not check_valid:
        status_code = 404
        response_message['message'] = 'This wishlist does not exist.'
        resp = make_response(response_message)
        resp.status_code = status_code
        database.session.close()
        return resp
    products = WishlistItems.query.filter_by(wishlist_id=wishlist_id).all()
    response_data['id'] = check_valid.id
    response_data['wishlist_id'] = check_valid.wishlist_id
    response_data['owner_id'] = check_valid.owner_id
    response_data['wishlist_name'] = check_valid.wishlist_name
    response_data['wishlist_description'] = check_valid.wishlist_description
    response_data['first_name'] = check_valid.first_name
    response_data['last_name'] = check_valid.last_name
    response_data['address'] = check_valid.address
    response_data['phone'] = check_valid.phone
    response_data['postcode'] = check_valid.postcode
    response_data['state'] = check_valid.state
    response_data['payer_fname'] = check_valid.payer_fname
    L = []
    for p in products:
        p_list = {"products_id": p.products_id,
                  "product_name": p.product_name,
                  "product_cover": p.product_cover,
                  "size": p.size,
                  "price": p.price,
                  "count": p.count}
        # "products_id": fields.Integer,
        # "product_name": fields.String,
        # "product_cover": fields.String,
        # "size": fields.String,
        # "count": fields.Integer,
        # "price": fields.Float,
        L.append(p_list)
    response_data["products"] = L
    resp = make_response(response_data)
    resp.status_code = status_code
    resp.response_data = response_data
    database.session.close()
    return resp

def process_change_count(changeInf):
    response_message = {
        "message": "success"
    }
    status_code = 200
    # get input information
    uid = changeInf["wishlist_id"]
    pid = changeInf["products_id"]
    size = changeInf["size"]
    # query cart table to get user information
    this_row_wishlist_item = WishlistItems.query.filter_by(wishlist_id=uid, products_id=pid, size=size).first()
    # check the cart is empty or not
    if this_row_wishlist_item is None:
        response_message["message"] = "Input information not correct"
        status_code = 400
        # database.session.close()
    else:
        # the_product = Products.query.filter_by(id=pid).first()
        # the_price = the_product.price
        # change the amount of produnts and the total price
        this_row_wishlist_item.count = changeInf["count"]
        # cart.each_total_price = the_price * changeInf["count"]
        database.session.commit()
        # database.session.close()

    resp = make_response(response_message)
    resp.status_code = status_code
    resp.message = response_message['message']
    database.session.close()
    return resp