from DB.db_init import *

tags = db.Table('tags',
                db.Column('tag_name', db.Integer, db.ForeignKey('tag.name'), primary_key=True),
                db.Column('donation_id', db.Integer, db.ForeignKey('donation.id'), primary_key=True)
                )


class Tag(db.Model):
    name = db.Column(db.String, primary_key=True)


def get_all_tag_names():
    all_tags = Tag.query.all()
    tag_names = [tag.name for tag in all_tags]
    return tag_names


def get_or_add_tag(tag_name):
    """
    :return: get the tag object from the db or add it to the db and return it / exception
    """
    tag = Tag.query.filter_by(name=tag_name).first()
    if tag:
        return tag

    new_tag = Tag(name=tag_name)
    try:
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    except Exception as e:
        db_logger.error("func: add_new_tag failed with error %s" % e)
        raise e

