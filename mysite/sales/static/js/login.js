Vue.createApp({
    delimiters: ['[[', ']]'],
    components: {},
    data() {
        return {
            user_login: {
                email: '',
                password: '',
                check_status: false
            },
            register_user: {
                first_name: '',
                last_name: '',
                email: '',
                password: '',
                user_type: 4,
                birthday: '',
                address: '',
                phone: '',
                check_status: false
            },
            token: '',
            isLoading: false,
        }
    },
    watch: {},
    created() {
        this.initialization();
    },
    mounted() {
        // this.showModal()
    },
    computed: {},
    methods: {
        initialization() {
            let scop = this
            scop.token = $cookies.get("Breaker")
            $cookies.remove("Breaker")
        },
        login() {
            let scop = this
            scop.user_login.check_status = false
            if (scop.user_login.email != '' && scop.user_login.password != '') {
                axios({
                    method: "POST",
                    url: url_api, //django path name
                    headers: {'X-CSRFTOKEN': $cookies.get("csrftoken"), 'Content-Type': 'application/json'},
                    data: {
                        'status': 'login',
                        "user": scop.user_login.email,
                        "password": scop.user_login.password
                    },
                }).then(response => {
                    console.log(response)
                    scop.user_login.check_status = false
                    location.href = '/home'
                }).catch(err => {
                    console.log(err)
                    scop.user_login.check_status = true
                });
            } else
                scop.user_login.check_status = true

        },
        register() {
            let scop = this
            scop.register_user.check_status = true
            if (scop.register_user.first_name != '' && scop.register_user.last_name != '' && scop.register_user.email != '' && scop.register_user.password != '' && scop.register_user.birthday != '' && scop.register_user.phone != '' && scop.register_user.address != '') {
                scop.register_user.check_status = false
                scop.isLoading = true
                var form = new FormData();
                form.append("account", scop.register_user.email);
                form.append("password", scop.register_user.password);
                form.append("user_type", scop.register_user.user_type);
                form.append("status", "user_active");

                var settings = {
                    "url": "api/account",
                    "method": "POST",
                    "timeout": 0,
                    "headers": {
                        "Authorization": "Bearer " + scop.token,
                        "X-CSRFToken": $cookies.get("csrftoken")
                    },
                    "processData": false,
                    "mimeType": "multipart/form-data",
                    "contentType": false,
                    "data": form
                };

                $.ajax(settings).then(function (response) {
                    console.log(response);

                    var form_user = new FormData();
                    form_user.append("name", scop.register_user.first_name + " " + scop.register_user.last_name);
                    form_user.append("address", scop.register_user.address);
                    form_user.append("birthday", scop.register_user.birthday);
                    form_user.append("status", "user_active");
                    form_user.append("type_user", scop.register_user.user_type);
                    form_user.append("phone", scop.register_user.phone);
                    form_user.append("user", scop.register_user.email);
                    form_user.append("email", scop.register_user.email);

                    var settings_user = {
                        "url": "api/user",
                        "method": "POST",
                        "timeout": 0,
                        "headers": {
                            "Authorization": "Bearer " + scop.token,
                            "X-CSRFToken": $cookies.get("csrftoken")
                        },
                        "processData": false,
                        "mimeType": "multipart/form-data",
                        "contentType": false,
                        "data": form_user
                    };

                    $.ajax(settings_user).then(function (response) {
                        console.log(response);
                        Swal.fire({
                            position: 'top-end',
                            icon: 'success',
                            title: 'Tạo tài khoản mới thành công',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        setTimeout(function () {
                            location.href = '/home'
                        }, 2000);
                    }).catch(err => {
                        console.log(err)
                    }).done(function () {
                        scop.isLoading = false
                    });
                }).catch(err => {
                    console.log(err)
                }).done(function () {
                });
                axios({
                    method: "POST",
                    url: url_api, //django path name
                    headers: {'X-CSRFTOKEN': $cookies.get("csrftoken"), 'Content-Type': 'application/json'},
                    data: {
                        'status': 'register',
                        "user": scop.register_user.email,
                        "password": scop.register_user.password
                    },
                }).then(response => {
                    console.log(response)
                }).catch(err => {
                    console.log(err)
                    scop.isLoading = false
                });
            } else {
                scop.isLoading = false
            }

        }
    }
}).mount('#login_page');
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
const popover = new bootstrap.Popover('.popover-dismiss', {
    trigger: 'focus'
})