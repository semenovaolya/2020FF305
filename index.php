<?php
require_once('classes.php');
?>
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
    </head>
    <body>
        <div>
            <form name="form" enctype="multipart/form-data" action="" method="POST">
                <div class="filter" style="display:block">
                        <label for="count-logs">Введите количество фильтруемых логов (по умолчанию - 50)</label>
                        <input type="number" id="count-logs" name="count-logs" min="1"></br></br>
                        <label for="type-message">Выберите тип лога</label>
                        <select id="type-message" name="type-message">
                            <option></option>
                            <option>Info</option>
                            <option>Warning</option>
                            <option>Error</option>
                        </select><br><br>
                        <span>Укажите период:</span>
                        <label for="start-period">С</label>
                        <input id="start-period" name="start-period" type="date">
                        <label for="end-period">по</label>
                        <input id="end-period" name="end-period" type="date"></br></br>
                        <input name="search" type="text" placeholder="Введите текст для поиска"></br></br>
                        <button type="reset">Сбросить</button>
                        <input name="filter" type="submit" value="Вывести логи"></br></br>
                </div>
                <div class="edit-logs" style="display:block"><u>Редактировать логи</u></div>
                <?
                if (isset($_POST['filter']) && $_POST['filter']) {
                   $file = new WorkWithLogs();
                foreach ($file->logs as $key => $log) { ?>
                <div>
                    <img class="hide delete" src="/images/delete.jpg" height="12">
                    <img class="hide edit" src="/images/empty_edit.png" height="12">
                    <span class="text-log"><?= $log ?></span>
                </div>
                <?}
                }?>
                <script type="text/javascript">
                    $(document).ready(function(){
                        $('.hide').hide();
                        $('.edit-logs').click(function(){
                            $('.hide').slideToggle();
                            return false;
                        });
                        $('.delete').click(function(){
                            $(this).parent().hide();
                            return false;
                        });
                        $('.edit').click(function(){
                            $(this).parent().children('.text-log').attr('style', 'color:#FFEBCD');
                            $(this).attr('src', '/images/edit.png');
                            return false;
                        });
                    });
                </script>
            </form>
        </div>
    </body>
</html>