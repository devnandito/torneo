//$(document).on("ready",inicio);
//function inicio()
//{
//	
//}
function popup(url)
{
	window.open(url,'name','height=830,width=808, menubar=yes, left=150,top=50');
	if (window.focus)
	{
		newwindow.focus()
	}
}
var Paginator =
{

    jumpToPage: function(pages)
    {
        var page = prompt("Enter a number between 1 and " + pages + " to jump to that page", "");
        if (page != undefined)
        {
            page = parseInt(page, 10)
            if (!isNaN(page) && page > 0 && page <= pages)
            {
                window.location.href = "?page=" + page;
            }
        }
    }

};
/*function marcar()
{
	alert('Hola');
}*/

/*function inicio()
{
	$("#personalizar").on("click", transicion);

}
/*function transicion ()
{
	var cambiosCSS =
	{
		margin: 0,
		overflow:"hidden",
		padding: 0,
		width: 0
	};
	var cambiosPerson = 
	{
		height: "auto",
		opacity: 1,
		width: "40%"
	};
	$("#historia").css(cambiosCSS);
	$("#personalizacion").css(cambiosPerson);
	$("#color div").on("click", cambiarColor);
}
function cambiarColor (datos)
{
	var col = datos.currentTarget.id;
	$("#cochecito img").attr("src", "img/c" + col + ".jpg"	);
}
function mostrar(www){
	$.ajax
	({
		url: www,
		type: "GET",
		success: llegada
	});
}
function llegada(datos)
{
	$("#resultado").empty();
	$("#resultado").html(datos);
}*/
