import os

from xddtools.entries import Animation

if __name__ == '__main__':
    for anim in os.listdir("./"):
        if not os.path.isdir(anim):
            continue
        a = Animation(anim_dir=anim)
        print(f"{anim}:{a.animations}")

    # def change_dict(d):
    #     tem = d["animations"]["g2"]
    #     # tem2 = d["animations"]["defend_Scourge_A1"]
    #     d["animations"] = {"anim": tem}
    #     return d
    #
    # a = Animation(anim_dir="skill_c2", dict_func=change_dict, is_fx=True)
    # a.copy_and_rename_animation("./")
    #
    # a = Animation(anim_dir="fx/default_anim_0")
    # print(a.animations)
