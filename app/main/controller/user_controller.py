# endpoint for user operations
from flask import request
from flask_login import login_required
from flask_restplus import Resource

from app.main.service.user_service import UserService
from app.main.util.dto import AuthDto, PostDto, UserDto

api = UserDto.api
user_auth = AuthDto.user_auth
user = UserDto.user
userInfo = UserDto.userInfo
payment = UserDto.payment
post = PostDto.article


@api.route('/<id>')
class GetUserDetails(Resource):
    """ Fetch details of user by id """
    @api.doc('Endpoint to fetch details of a user by id')
    @api.marshal_with(userInfo, envelope='resource')
    def get(self, id):
        # Fetching the user id
        return UserService.get_by_id(id=id)


@api.route('/getFeed')
class GetUserFeed(Resource):
    """ Get the user's feed based on priority of tags """
    @login_required
    @api.doc('Endpoint to get the user\'s feed based on tag priority')
    @api.marshal_with(post, envelope='resource')
    def get(self):
        return UserService.get_user_feed()


@api.route("/update")
class UpdateUserInfo(Resource):
    @login_required
    @api.doc(params={"update_dict": "Key value pairs of all update values"})
    @api.expect(userInfo)
    def post(self):
        update_dict = request.json
        return UserService.update_user_info(update_dict)


@api.route("/payment")
class Payment(Resource):
    @login_required
    @api.expect(payment)
    def post(self):
        post_data = request.json
        return UserService.save_user_payment(data=post_data)


@api.route('/get_payment')
class GetPayment(Resource):
    """ Getting the payments of user """
    @login_required
    @api.doc('Endpoint to get the payments done by a user.')
    @api.marshal_with(payment, envelope='resource')
    def get(self):
        return UserService.get_user_payment()


@api.route('/followedTags')
class FollowedTags(Resource):
    """ Getting tags followed by user """
    @login_required
    @api.doc('Endpoint to get the tags followed by a user')
    def get(self):
        return UserService.get_user_tags()
