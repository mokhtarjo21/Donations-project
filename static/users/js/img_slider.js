
$('buttonphoto').css('display', 'none');
var coun=1;
$('imgphoto').click(function(){
    $('buttonphoto').fadeIn();
    $('divphotp').css({
        'display': 'block',
       'z-index': '50',
       
        'width': '100%',
        'height': '100%',
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'background-color': 'rgba(0,0,0,0.5)',
        
    })
    $('divphotp').html(`<img src='${$(this).attr('src')}' width="400px" height="400px" style="position: absolute;
     top: 50%; left: 50%; transform: translate(-50%, -50%);z-index:200">
   
   
    
    `);
    
   
});

function next(){
    coun=$('divphotp img').attr('src').split('/')[2].split('.')[0];
    if(coun==4){
        coun=0;
        
    }
    $('divphotp img').attr('src', './img/'+(++coun)+'.jpg');
   $('divphotp').off("on")
}
function Previos(){
    coun=$('divphotp img').attr('src').split('/')[2].split('.')[0];
    if(coun==1){
        coun=5;
        
    }
    $('divphotp img').attr('src', './img/'+(--coun)+'.jpg');
}
$('divphotp').click(function(e){
   
    $('divphotp').fadeOut();
    $('button').fadeOut();
    })

