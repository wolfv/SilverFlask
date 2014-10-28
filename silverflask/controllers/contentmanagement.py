from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask import jsonify

bp = Blueprint('cms', __name__)

@bp.route("testcms")
def test():
    return "TEST"