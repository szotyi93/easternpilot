from common.op_params import opParams
from selfdrive.controls.lib.dynamic_follow.support import dfProfiles
from selfdrive.controls.lib.dynamic_follow.df_manager import dfManager


def enable_eastern_roads(eastern_road_flag=True, debug=False):
    op_params = opParams()
    df_profiles = dfProfiles()
    df_manager = dfManager(op_params)
    if eastern_road_flag:
        if df_manager.cur_user_profile == df_profiles.traffic:
            op_params.put('camera_offset', int(0.06))
        elif df_manager.cur_user_profile == df_profiles.relaxed:
            op_params.put('camera_offset', int(0.2))
        elif df_manager.cur_user_profile == df_profiles.roadtrip:
            op_params.put('camera_offset', int(0.4))
        elif df_manager.cur_user_profile == df_profiles.auto:
            op_params.put('camera_offset', int(1))
        else:
            pass
    if debug:
            print(op_params.get('camera_offset'))
    else:
        pass


if __name__ == '__main__':
    enable_eastern_roads(True, True)
