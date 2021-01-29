from common.op_params import opParams
from selfdrive.controls.lib.dynamic_follow.support import dfProfiles
from selfdrive.controls.lib.dynamic_follow.df_manager import dfManager
import cereal.messaging as messaging


def enable_eastern_roads(eastern_road_flag=True, debug=False):
    sm_smiskol = messaging.SubMaster(['dynamicFollowButton'])
    op_params = opParams()
    df_profiles = dfProfiles()
    df_manager = dfManager(op_params)
    if eastern_road_flag:
        if sm_smiskol['dynamicFollowButton'].status == df_profiles.traffic:
            op_params.put('camera_offset', 0.06)
        elif sm_smiskol['dynamicFollowButton'].status == df_profiles.relaxed:
            op_params.put('camera_offset', 0.2)
        elif sm_smiskol['dynamicFollowButton'].status == df_profiles.roadtrip:
            op_params.put('camera_offset', 0.6)
        elif sm_smiskol['dynamicFollowButton'].status == df_profiles.auto:
            op_params.put('camera_offset', 1.3)
        else:
            pass
    if debug:
            print(op_params.get('camera_offset'))
    else:
        pass


if __name__ == '__main__':
    enable_eastern_roads(True, True)
