from sample import utils

# Hook decorators
def disable_other_hooks(hook_func):
    def decorator(instance):
        setattr(instance, 'SKIP_HOOKS', True)
        hook_func(instance)
        setattr(instance, 'SKIP_HOOKS', False)
    return decorator

# General functions
def hook_auto_save(instance):
    assert hasattr(instance, 'UPDATE_JSON_ON_ATTRIBUTE_SET'), "Instance must have UPDATE_JSON_ON_ATTRIBUTE_SET attribute"
    if getattr(instance, 'UPDATE_JSON_ON_ATTRIBUTE_SET', False):
        utils.save(instance)

# Camera specific hooks
@disable_other_hooks
def hook_auto_calculate_fov(instance):
    assert hasattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS'), "Instance must have AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS attribute"
    if getattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS', False):
        instance.calculate_fov()

@disable_other_hooks
def hook_auto_calculate_focal_length(instance):
    assert hasattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS'), "Instance must have AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS attribute"
    if getattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS', False):
        instance.calculate_focal_length()

@disable_other_hooks
def hook_auto_calculate_sensor_size(instance):
    assert hasattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS'), "Instance must have AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS attribute"
    if getattr(instance, 'AUTO_CALCULATE_ATTRIBUTES_FROM_OTHERS', False):
        instance.calculate_sensor_size()