Vue.createApp({
    delimiters: ['[[', ']]'],
    components: {},
    data() {
        return {
            token: '',
            isLoading: false,
            shoppingCart: {
                commodity_name_id: '',
                user_id: '',
                count_cart: '',
                ShoppingCart: '',
            },
            count_cart: 0,
            data_cart: [],
        }
    },
    watch: {},
    created() {
    },
    mounted() {
        this.initialization();
    },
    computed: {},
    methods: {
        initialization() {
            let scop = this
            let num = 1000;
            let vndFormattedNum = num.toLocaleString('vi-VN', {style: 'currency', currency: 'VND'});
            scop.token = $cookies.get("Breaker")
            $cookies.remove("Breaker")
            scop.data_cart = scop.readJSONFromElement($('#data-com'), 'data-com') || []
            scop.data_cart.forEach(function (item, index) {
                item.price = item.price.toLocaleString('vi-VN', {style: 'currency', currency: 'VND'});
            })
            console.log(scop.data_cart)
            $.getJSON("https://api.ipify.org?format=json", function (data) {

                // Setting text of element P with id gfg
                console.log('ip: ', data);
                localStorage.setItem("local store", data.ip)
            })
        },
        readJSONFromElement(el, title) {
            try {
                if (!el.text()) return null
                return JSON.parse(el.text().replace(/True/gm, 'true').replace(/False/gm, 'false').replace(/\'/gm, '"').replace(/None/gm, 'null') || '{}')
            } catch (e) {
                console.log(title, e);
                return null;
            }
        },
        addShoppingCarts() {
            let scop = this
            scop.count_cart += 1
        }
    }
}).mount('#home_page');


const myCarouselElement = document.querySelector('#myCarousel')

// const carousel = new bootstrap.Carousel(myCarouselElement, {
//   interval: 2000,
// })
var carouselWidth = $(".carousel-inner.item-store")[0].scrollWidth;
var cardWidth = $(".carousel-item.item-store").width();
var scrollPosition = 0;
$(".carousel-control-next.item-store").on("click", function () {
    if (scrollPosition < (carouselWidth - cardWidth * 4)) { //check if you can go any further
        scrollPosition += cardWidth * 7;  //update scroll position
        $(".carousel-inner.item-store").animate({scrollLeft: scrollPosition}, 600); //scroll left
    }
});
$(".carousel-control-prev.item-store").on("click", function () {
    if (scrollPosition > 0) {
        scrollPosition -= cardWidth * 7;
        $(".carousel-inner.item-store").animate(
            {scrollLeft: scrollPosition},
            600
        );
    }
});
var multipleCardCarousel = document.querySelector(
    "#carouselExample"
);
if (window.matchMedia("(min-width: 768px)").matches) {
    //rest of the code
    var carousel = new bootstrap.Carousel(multipleCardCarousel, {
        interval: false
    });
}