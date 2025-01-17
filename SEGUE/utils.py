from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    if not instance:
        return {}
        
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields: #+ opts.many_to_many:
    
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                print(instance)
                data[f.name] = list(f.value_from_object(f).values_list('pk', flat=True))
        else:
            name = f.name + '_id' if f.is_relation else f.name
            data[name] = f.value_from_object(instance)
    return data
