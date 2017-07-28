/**
 * Created by cocacola on 17-1-8.
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

function getAllOrder(url, page){
    /**
     * 显示该用户的全部订单
     * */
    $.get(url, {page: page}, function(data){
        $('.main_con .right_content .order_list').html(data);

        var prices = $('.order_goods_list .col02 cite');
        var counts = $('.order_goods_list .col03');
        var totals = $('.order_goods_list .col04');
        totals.each(function(index){
            var price = prices.eq(index).text();
            var count = counts.eq(index).text();
            var total = parseFloat(price)*parseFloat(count);
            totals.eq(index).text(changeTwoDecimal(total)+'元');
        })
        var page_count = parseInt($('.pageinfo em').text());
        var page_index = parseInt($('.pageinfo cite').text());
        var pagenation = $('.pagenation');
        pagenation.empty();
        if (page_index == 1){pagenation.append('<a><上一页</a>');}
        else{pagenation.append('<a href="javascript:;" onclick="getAllOrder(\''+url+'\','+(page_index-1).toString()+')"'+'><上一页</a>')}

        for(p=1;p<=page_count;p+=1){
            if(p==page_index){text = '<a class="active">'+p.toString()+'</a>'}
            else{text='<a href="javascript:;" onclick="getAllOrder(\''+url+'\','+p.toString()+')">'+p.toString()+'</a>'}
            pagenation.append(text);
        }

        if (page_index >= page_count){pagenation.append('<a>下一页></a>');}
        else{pagenation.append('<a href="javascript:;" onclick="getAllOrder(\''+url+'\','+(page_index+1).toString()+')"'+'>下一页></a>')}
    })
}

$(function(){
    url = '/order/get_order/';
    getAllOrder(url, 1);
});