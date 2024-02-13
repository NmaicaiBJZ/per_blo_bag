// 整个侧边栏
let sidebar = document.querySelector('.sidebar');
// 用于侧边栏的滚动
let scrollY = 0;
// 需要上下移动内容
let scroll_con = document.querySelector('.scroll_con');

function add_rotation_sp(){
    let arr_p = document.querySelectorAll('.sidebar_title');
    // 为最新随笔与随笔分类添加单击方法，单击后三角形旋转，下拉有动画
    for(const i of arr_p){
        i.addEventListener('click',function(){
            if(!(i.childNodes[1].classList.contains("menu_rotation_spin"))){
                // 添加三角形旋转
                i.childNodes[1].classList.add("menu_rotation_spin");
                // 最新随笔与随笔分类添加动画
                i.parentElement.classList.add("sidebar_count_anim");
            }else{
                i.childNodes[1].classList.remove("menu_rotation_spin");
                i.parentElement.classList.remove("sidebar_count_anim");
            }
        })
    }
}

function add_class_list_am(){
    let arr_ul = document.querySelectorAll('.sidebar_count > ul ul');
    // 为随笔分类中的每个分类添加单击方法，单击后有下拉收放动画
    for(const i of arr_ul){
        i.previousElementSibling.addEventListener('click',function(){
            if(!(i.classList.contains("classified_list_anim"))){
                // 为分类列表添加下拉动画
                i.classList.add("classified_list_anim");
            }else{
                i.classList.remove("classified_list_anim");
            }
        })
    }
}
// 为侧边栏的添加鼠标滚轮监听事件，当鼠标上下滚动时，屏幕随之滚动
sidebar.addEventListener('wheel', (e) => {
    e.preventDefault();

    // 根据滚轮方向调整滚动值
    scrollY -= e.deltaY;

    // 限制滚动范围
    scrollY = Math.min(0, Math.max(scrollY, -scroll_con.clientHeight + sidebar.clientHeight));

    // 更新滚动位置
    scroll_con.style.transform = `translateY(${scrollY}px)`;
})



let primary = document.querySelector('.primary');

let sidebar_call = document.getElementById('sidebar_call');
sidebar_call.addEventListener('click',function(){
    sidebar.style = "display: block";
    sidebar_call.style = "display: none";
    
    primary.addEventListener('click',function parmaryListener(){
        sidebar.style = "display: none";
        sidebar_call.style = "display: inline-block";
        primary.removeEventListener('click',parmaryListener);
    })
})