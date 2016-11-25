import Publish_Anim_Update_EnvOnlyHaveLowMdl as paue
import pymel.core as pm


def run():
    paue.replace_all_with_low_env()
    pm.warning('Done replacing All EnvAsset to low model status,please check..')
