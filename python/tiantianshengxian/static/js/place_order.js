/**
 * Created by cocacola on 17-1-6.
 */
function changeTwoDecimal(strVar){
    /** 对小数四舍五入，并保留两位小数*/
    var num = parseFloat(strVar);
    if (isNaN(num)){
        console.log(strVar,'is a invild num');
        return 0;
    }
    var strNum = (Math.round(num*100)/100).toString();
    var pos_decimal = strNum.indexOf('.');
    if(pos_decimal < 0){
        pos_decimal = strNum.length;
        strNum += '.';
    }
    while(strNum.length <= pos_decimal+2){
        strNum += '0';
    }
    return strNum;
}

$(function(){
    var goods_count = 0;   // 订单商品数量
    var total_price = 0;    // 订单总价
    var transit = 12;    // 邮费
    var total_pay = 0;    // 订单最终支付价格

    var listNum = $('.goods_list_td .col01');
    var strPrice = $('.goods_list_td .col05');
    var strCount = $('.goods_list_td .col06');
    var strTotal = $('.goods_list_td .col07');

    // 计算同件商品的总价
    strTotal.each(function(index){
        var price = parseFloat(strPrice.eq(index).text());
        var count = parseFloat(strCount.eq(index).text());
        goods_count += count;
        var total = parseFloat(price*count);
        total_price += total;
        $(this).text(changeTwoDecimal(total));
        listNum.eq(index).text(index+1);
    });

    $('.total_goods_count em').text(changeTwoDecimal(goods_count));   // 订单商品数量
    $('.total_goods_count b').text(changeTwoDecimal(total_price));    // 订单总价
    $('.transit b').text(transit);    // 邮费
    $('.total_pay b').text(changeTwoDecimal(total_price+transit));    // 订单最终支付价格

});

$(function(){
   $('#order_btn').click(function() {
       url = window.location.href;
       authCode = url.split('?')[1].split('=')[1];

       $.get('/order/submit/',{authCode:authCode},function(data){
           console.log(data)
           localStorage.setItem('order_finish',2);
           $('.popup_con').fadeIn('fast', function() {
               setTimeout(function(){
                   $('.popup_con').fadeOut('fast',function(){
                       window.location.href = '/users/manage/orders/';
                   });
               },3000)
            });
       });
   });

   $('.common_list_con dd input').each(function(index,item){
       console.log($(item).val());
       console.log($(item).checked);
   })

});