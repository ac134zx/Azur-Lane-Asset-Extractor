import os
import subprocess
import time
import sys
#import hashlib

o1dir=input('dir of assets and output:')
spath = os.path.abspath(__file__)
sdir = os.path.dirname(spath)
print(sdir)

Awdr='/storage/emulated/0/Android/data/com.bilibili.azurlane/files/AssetBundles'

'/storage/emulated/0/Android/data/com.bilibili.azurlane/files/AssetBundles'

#文件更新（完工）
#os.system('adb pull /storage/emulated/0/Android/data/com.bilibili.azurlane/files/AssetBundles/ %s'%o1dir)

a_dir_list=['char','painting','spinepainting','emoji','gallerypic','loadingbg','commanderpainting','live2d','bg','mangapic','shrine2022','plane','cue']
#a_dir_list=['char']
def repack_atlas(ipt,ftp='.atlas'):#spine解包纹理,但是不好用的样子(由于spine软件问题，该功能暂时无法使用)
        for r,d,f in os.walk(ipt):
            for im in f:
                if im.endswith(ftp):
                    atlas_d=f'{r}\\{im}'
                    cmmd=f'spine -i {r} -o {r} -c {atlas_d}'
                    subprocess.run(cmmd,stdout=subprocess.PIPE)
                    os.system(r'\spine\install.bat')   

def spine_lower_4t3(maindir,v='3.8.75'):
    dir_list=['spinepainting']
    for ki in dir_list:
        fd=maindir+'\\'+ki
        #print(fd)
        for r,d,f in os.walk(fd):
            for ki in f:
                s=ki.split(".")
                #print(s,'\n',s[-1])
                if s[-1]=='atlas':
                    print('pcs atlas %s'%ki)
                    os.system('%s\SpineSkeletonDataConverter\sad3.exe %s %s'%(sdir,r+'\\'+ki,r))
                elif s[-1]=='skel':
                    print('pcs skel %s'%ki)
                    opts=r+s[0]+'.json'
                    os.system("%s\SpineSkeletonDataConverter\ssd3.exe %s %s -v %s"%(sdir,r+'\\'+ki,opts,v))
def export_uty_asst(mdr,dir_list,updatefile=[]): #文件夹
    def export(walk_sub_d,optd):

        if subd=='live2d':
             cmmd=f'{sdir}\AssetStudioModCLI\AssetStudioModCLI.exe {walk_sub_d} -o {optd} -m Live2d'
        elif subd=='cue':
            pass
        
        else:
             cmmd=f'{sdir}\AssetStudioModCLI\AssetStudioModCLI.exe {walk_sub_d} -o {optd} -t tex2d,textAsset,mesh -m Export'
    
        cmmd_ret=subprocess.Popen(cmmd)
        cmmd_ret.wait()

    def update(file):
        if file !=[]:
            for i in file:
                name=i.split('\\')
                opt=f'{mdr}\\opt_asst\{name[-2]}'
                print(opt)
                if 'live2d' in file:
                    cmmd=f'{sdir}\AssetStudioModCLI\AssetStudioModCLI.exe {i} -o {opt} -m Live2d'

                else:
                    cmmd=f'{sdir}\AssetStudioModCLI\AssetStudioModCLI.exe {i} -o {opt} -t tex2d,textAsset,mesh -m Export'
                cmmd_ret=subprocess.Popen(cmmd)
                cmmd_ret.wait()         
                #print(cmmd_ret.returncode)  #update导出文件，但是bug不能用x

    if updatefile==[]:
        for subd in dir_list:
            if subd=='cue':
                pass
            print(f'pcs:{subd}')
            opt=f'{mdr}\opt_asst\{subd}'
            full_subd=f'{mdr}\{subd}'
            export(full_subd,opt)
    else:
            update(updatefile)

def wavf(ipd,opd,updtf=[]):
    win_wav_f_d=[]
    if not os.path.exists(opd):
        os.makedirs(opd)
        
    for r,d,f in os.walk(opd):
        for i in f:
            win_wav_f_d.append(i.split(".")[0])

    def updt(nf):
        for i in nf:
            
            if i.endswith('.b'):
                print('updt f')
                nd=i.split('.')[0]+'.acb'
                if not os.path.exists(nd):
                    os.rename(i,nd)
          


    def FExpt():                
        for r,d,f in os.walk(ipd):
                for i in f:
                    fulld=f'{r}\{i}'
                    nf=i.split('.')[0]
                    nfd=f'{r}\{nf}.acb'
                    if fulld.endswith('.b'):
                        if not os.path.exists(nfd):
                            os.rename(fulld,nfd)
                    cmmd=f'{sdir}\vgmstream-win\\vgmstream-cli.exe -o {opd}\{nf}.wav {nfd}'
                    #print(cmmd)
                    cmmd_ret=subprocess.run(cmmd,stdout=subprocess.PIPE)
                    print(cmmd_ret.stdout.decode().rstrip('\n').split('\n')[0])
                    os.rename(nfd,fulld)
    if updtf==[]:
        FExpt()
    else:
        updt(updtf)

def func_update(maindir,aipd,dir_list,shot_opt=0,chk=0):
    t1=time.time()
    pulled_file=[]
    for subf in dir_list:
        full_sfd=maindir+'\\'+subf#子文件夹地址win
        if os.path.exists(full_sfd):
            print(f'find path:{full_sfd}')
        else:
            os.makedirs(full_sfd) #不在就创建

        sizefile='size_'+subf+'.txt'

        Win_list_file=[]
        N_list_file=[]

        if not os.path.exists(sizefile):
            open(sizefile,'w')  
            print(f'FNF,on creat {sizefile}') #hash file

        hashf=open(sizefile,'w')
        for r,d,f in os.walk(full_sfd):#local_F_D(W_list_files)
            for i in f:
                Win_list_file.append(i)
                size=os.path.getsize(f'{r}\{i}')
                hashf.writelines(f'{size}\n')


        hashf.close()
        print(f'size {subf} has write')
                                                #size write

        m=os.popen('adb shell find %s/%s'%(aipd,subf))
        fm=m.read().split('\n')
        fm.remove('')
        #fm.remove(f'{Awdr}/{subf}')
        print('search in %s:'%subf)
        #print(Win_list_file[2])
        if subf!='cue':
            for k in fm:
                #print(k)
                tail_name_A=k.split('/')[-1]#ADB文件夹名称             
                        #print(tail_name_A)
                if tail_name_A in Win_list_file:#加入#sha256计算(太tm慢了)/大小计算
                    if chk!=0:
                        sizehash=subprocess.run(f'adb shell ls -l {k}',stdout=subprocess.PIPE).stdout.decode().split(' ')[4]
                        wn=k.split("/")[-1]
                        win_size=os.path.getsize(f'{full_sfd}\{wn}')
                        if not int(sizehash)==int(win_size):
                            N_list_file.append(tail_name_A)
                            print(f'{tail_name_A} size chk fail adb:{sizehash} win:{win_size}')
                else:
                    if shot_opt !=0:
                        print('new res %s'%tail_name_A)
                        
                    N_list_file.append(tail_name_A)
        else:
            for k in fm:
                #print(k)
                tail_name_A=k.split('/')[-1].split(".")[0]+'.b'#ADB文件夹名称             
                #print(tail_name_A,Win_list_file[0])
                if tail_name_A in Win_list_file:#加入#sha256计算(太tm慢了)/大小计算
                    if chk!=0:
                        sizehash=subprocess.run(f'adb shell ls -l {k}',stdout=subprocess.PIPE).stdout.decode().split(' ')[4]
                        wn=k.split("/")[-1]
                        win_size=os.path.getsize(f'{full_sfd}\{wn}')
                        if not int(sizehash)==int(win_size):
                            N_list_file.append(tail_name_A)
                            print(f'{tail_name_A} size chk fail adb:{sizehash} win:{win_size}')
                else:
                    if shot_opt !=0:
                        print('new res %s'%tail_name_A)
                        
                    N_list_file.append(tail_name_A)
        if subf=='cue' :
            N_list_file.remove(f"{subf}.b")
        else:
            N_list_file.remove(subf)

        for ss in N_list_file:
                    sfd=Awdr+'/'+subf+'/'+ss
                    cmmd='adb pull %s %s'%(sfd,maindir+'\\'+subf)
                    if shot_opt !=0:
                        pass
                        #print(cmmd)
                    k=subprocess.Popen(cmmd,stdout=subprocess.PIPE)#stdout=subprocess.PIPE
                    #k.wait()

                    wfd=f"{maindir}\\{subf}\\{ss}"
                    pulled_file.append(wfd)
        f_pud=open(f'pud_{subf}.txt','w')
        for i in pulled_file:
            f_pud.writelines(i)
            f_pud.writelines('\n')
    t2=time.time()
    print(t2-t1)
    if pulled_file==[]:
        pulled_file==0

    return pulled_file
    
def func_pull(maindir,aipd,dir_list,shot_opt=0,chk=0): #pull还没有size chk（懒
    for i in dir_list:
        wdir=f'{maindir}\\{i}'
        if not os.path.exists(wdir):
            os.makedirs(wdir)
        fullfile=f'{aipd}/{i}'
        cmmd=f'adb pull {fullfile} {maindir}'
        subprocess.run(cmmd)

#spine_lower_4t3()
#repack(opd_asset)                
#end


#静态拼接 mesh拖进blender有奇效       
import traceback
from pathlib import Path
from typing import *
import cv2
import numpy as np


mdr=Path(f'{o1dir}/opt_asst/painting/Assets/ArtResource/Atlas/Paintings')
pdr=Path(f'{o1dir}/opt_asst/painting/Assets/ArtResource/Atlas/Paintings')
edr=Path(f'{o1dir}/opt_asst/painting/spelled')
def func_spell(pd,md,opt):
    t1=time.time()

    def read_mesh_obj(path):
        vertex = []  # x, y, x
        vertex_texture = []  # u, v
        vector_normal = []  # x, y, z # 2D 没有法向量
        face = []  # v/vt/vn
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                type_, *values = line.strip().split(" ")

                if type_ == "v":
                    vertex.append(list(map(int, values[:2])))
                elif type_ == "vt":
                    vertex_texture.append(list(map(float, values)))
                elif type_ == "f":
                    face.append([list(map(int, value.split("/"))) for value in values])
                else:
                    continue
        return vertex, vertex_texture, face

    def restore_painting(texture: np.ndarray, v, vt, f) -> np.ndarray:
        v = np.array(v)[:, 0:2]  # 去除 z 轴
        vt = np.array(vt)
        f = np.array(f)[:, :, 0:2]  # 去除法向量

        # 处理 v
        v = np.abs(v)  # 水平镜像, 原因不明
        v[:, 1] = np.max(v[:, 1]) - v[:, 1]  # 翻转 y 轴, x 对应列数, y 对应行数

        # 处理 vt
        vt = vt * np.array(texture.shape[1::-1]).reshape(1, 2)  # 转换到像素
        vt[:, 1] = texture.shape[0] - vt[:, 1]  # 翻转 y 轴
        vt = np.round(vt, 0).astype(int)  # 转换整数坐标

        # 新建空图
        width, height = np.max(v, axis=0) + 2  # 上下左右各扩展 1 个位置
        png = np.zeros((height, width, 4), dtype=texture.dtype)
        # print(png.shape)

        for i in range(0, len(f), 2):
            v_rect_pts: List[Tuple[int, int]] = []
            vt_rect_pts: List[Tuple[int, int]] = []

            for v_idx, vt_idx in f[i]:
                v_rect_pts.append(v[v_idx - 1])  # 下标需要序号 -1
                vt_rect_pts.append(vt[vt_idx - 1])

            for v_idx, vt_idx in f[i + 1]:
                v_rect_pts.append(v[v_idx - 1])
                vt_rect_pts.append(vt[vt_idx - 1])

            # 排序得到左上和右下坐标
            leftup_v, *_, rightdown_v = sorted(v_rect_pts, key=list)
            leftup_vt, *_, rightdown_vt = sorted(vt_rect_pts, key=list)

            # 转换像素行列坐标, 左闭右开
            leftup_v = (leftup_v + 1) - 1  # +1 是为了把图往两个正方向移动一格, 修正坐标
            rightdown_v = (rightdown_v + 1) + 1
            leftup_vt = leftup_vt - 1
            rightdown_vt = rightdown_vt + 1

            # 判断区域是否大小相等
            size1 = rightdown_v - leftup_v
            size2 = rightdown_vt - leftup_vt
            if not all(size1 == size2):
                # 处理不相等情况, 目前只发现纹理区域会可能多一行/列, 想办法去掉空白
                # 空白的条件是某一行/列透明度均小于一个阈值
                texture_region = texture[leftup_vt[1]:rightdown_vt[1], leftup_vt[0]:rightdown_vt[0]]
                alpha_value = 12

                row_delta = size2[1] - size1[1]
                if row_delta == 1:
                    if np.all(texture_region[-1, :, -1] < alpha_value):
                        rightdown_vt[1] -= 1
                    elif np.all(texture_region[0, :, -1] < alpha_value):
                        leftup_vt[1] += 1
                    else:
                        raise ValueError("Empty row not found!")
                elif row_delta > 1:
                    raise ValueError(f"{row_delta} extra rows found.")

                col_delta = size2[0] - size1[0]
                if col_delta == 1:
                    if np.all(texture_region[:, -1, -1] < alpha_value):
                        rightdown_vt[0] -= 1
                    elif np.all(texture_region[:, 0, -1] < alpha_value):
                        leftup_vt[0] += 1
                    else:
                        raise ValueError("Empty col not found!")
                elif col_delta > 1:
                    raise ValueError(f"{col_delta} extra cols found.")

            png[leftup_v[1]:rightdown_v[1], leftup_v[0]:rightdown_v[0]] = texture[leftup_vt[1]:rightdown_vt[1], leftup_vt[0]:rightdown_vt[0]]

        return png

    def func_s_1(picdir,meshdir,expt):
        if not os.path.exists(expt):
            os.makedirs(expt)

        count = 0
        ps,fl=0,0
        s0=picdir.iterdir()
        ndr_e_f=[]
        for r,dire,file in os.walk(expt):
            pass
        for pcg in s0:
                c=[]
                c.append(pcg)
                c.append(os.stat(pcg).st_size)
                if not '#' in pcg.name:
                    ndr_e_f.append(c)

                
        for mng in ndr_e_f:
                png=mng[0]
                
                #print(char_name)


                if png.name in file:
                    #print(f'IAE in {png.name}')
                    count+=1
                    fl+=1

                else:
                    if png.name.endswith('.png'):
                        char_name = png.stem
                        #print(png.name)
                        painting_path = expt.joinpath(png.name)

                        for mesh in meshdir.glob(f"{char_name}-mesh*.obj"):
                            v, vt, f = read_mesh_obj(mesh)
                            texture: np.ndarray = cv2.imread(png.as_posix(), cv2.IMREAD_UNCHANGED)

                            try:
                                painting = restore_painting(texture, v, vt, f)

                                ps+=1

                            except ValueError as E:
                                traceback.print_exc()
                                print(f"Restore Error: {char_name}")

                                fl+=1
                                      # 还原失败继续试下一个可能的 mesh 文件

                            # 还原成功跳出循环
                            cv2.imwrite(painting_path.as_posix(), painting)
                            count += 1
                            #break
        t2=time.time()

        print(f"Total: {count},fail:{fl},pass:{ps},{t2-t1}")  

    func_s_1(pd,md,opt)
if input('do you want to PULL all file and EXPORT it 是否拉取全部资源并解包:(y/n)')=='y':
    func_pull(o1dir,Awdr,a_dir_list)
    export_uty_asst(o1dir,a_dir_list)
    wavf(f'{o1dir}\cue',f'{o1dir}\opt_asst\cue')
if input('do you want to UPDATE all file and EXPORT it WITHOUT size check 是否以无大小检查的方式更新资源并解包（较快）:(y/n)')=='y':
    c01=func_update(o1dir,Awdr,a_dir_list,1)
    print(c01)
    export_uty_asst(o1dir,a_dir_list,updatefile=c01)
    wavf(f'{o1dir}\cue',f'{o1dir}\opt_asst\cue',updtf=c01)
if input('do you want to UPDATE all file and EXPORT it WITH size check 是否以大小检查的方式更新资源并解包（较慢）:(y/n)')=='y':
    c01=func_update(o1dir,Awdr,a_dir_list,1,1)
    print(c01)
    export_uty_asst(o1dir,a_dir_list,updatefile=c01)
    wavf(f'{o1dir}\cue',f'{o1dir}\opt_asst\cue',updtf=c01)

#cc01=func_update(o1dir,aipd=Awdr,dir_list=a_dir_list,shot_opt=10,chk=0)
#print(cc01)
#func_pull(o1dir,aipd=Awdr,dir_list=a_dir_list)
'''if input('if exp(y/n);') in 'yY':
    export_uty_asst(o1dir,dir_list=a_dir_list,updatefile=cc01) '''
if input('if spell_painting(y/n);') in 'yY':

    func_spell(pdr,mdr,edr)

#spine_lower_4t3(f'{o1dir}\opt_asst\spinepainting')
#repack_atlas(o1dir)


