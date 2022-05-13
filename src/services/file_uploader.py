import os
import uuid

from werkzeug.utils import secure_filename


def uploadImage(request):
    if 'file' not in request.files:
        return None
    else:
        file = request.files['file']
        if file.filename == '':
            return None
        if file:
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join('src/static/images', unique_filename))
            return unique_filename
        return None
