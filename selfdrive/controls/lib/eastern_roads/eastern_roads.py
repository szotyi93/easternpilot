from common.op_params import opParams
from selfdrive.controls.lib.dynamic_follow.support import dfProfiles
from selfdrive.controls.lib.dynamic_follow.df_manager import dfManager

op_params = opParams()
df_profiles = dfProfiles()
df_manager = dfManager(op_params)


def enable_eastern_roads(eastern_road_flag, debug=False):
    if eastern_road_flag:
        if debug:
            print(op_params.get('camera_offset'))
        if df_manager.cur_user_profile == df_profiles.traffic:
            op_params.put('camera_offset', 0.11)
        elif df_manager.cur_user_profile == df_profiles.relaxed:
            op_params.put('camera_offset', 0.4)
        elif df_manager.cur_user_profile == df_profiles.roadtrip:
            op_params.put('camera_offset', 1)
        elif df_manager.cur_user_profile == df_profiles.auto:
            op_params.put('camera_offset', 1.5)
        else:
            pass
    else:
        pass
