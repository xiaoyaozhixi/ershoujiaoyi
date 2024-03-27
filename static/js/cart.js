$('#boxall').click(
    function () {
        // this.checked:布尔类型，代表this指向的#boxall对象有没有checked属性
        if(this.checked){
            // 选中时，添加goods_check的checked属性
            $('.goods_check').prop('checked',true)
        }
        else{
            // 不选中时，去掉goods_check的checked属性
            $('.goods_check').prop('checked',false)
        }
    }
);

$('.goods_check').each(
  function () {
      $(this).click(
          function () {
              if(!this.checked){
                  $('#boxall').prop('checked', false)
              }
              add();
          }
      )
  }
);

function add() {
    var dic = {num:0,total:0};
    $('.goods_check').each(
        function () {
            if(this.checked){
                // 数量
                var num =parseInt($(this).parents('.cart_list_td').find('.num_show').val()) ;
                // 小计
                var total =parseFloat($(this).parents('.cart_list_td').find('.col07').text());
                dic.num+=num;
                dic.total+=total;
            }
        }
    );
    $('#total_mount').text(dic.total);
    $('#total_num').text(dic.num);
}

