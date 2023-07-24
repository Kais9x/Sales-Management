// This function is used to detect the actual image type,
function getMimeType(file, fallback = null) {
    const byteArray = new Uint8Array(file).subarray(0, 4);
    let header = '';
    for (let i = 0; i < byteArray.length; i++) {
        header += byteArray[i].toString(16);
    }
    switch (header) {
        case '89504e47':
            return 'image/png';
        case '47494638':
            return 'image/gif';
        case 'ffd8ffe0':
        case 'ffd8ffe1':
        case 'ffd8ffe2':
        case 'ffd8ffe3':
        case 'ffd8ffe8':
            return 'image/jpeg';
        default:
            return fallback;
    }
}

Vue.createApp({
    data() {
        return {
            image: {
                src: null,
                type: null,
            },
            result: null,
            goods: {
                image: '',
                name: '',
                type: '',
                brand: '',
                description: '',
                price: '',
                quantity: '',
                id: ''
            },
            user: {
                name: '',
                email: '',
                id: '',
            },
            userInfo: '',
            token: '',
            file: '',
            isLoading: false,
        };
    },
    mounted() {
        this.initialization()
    },
    methods: {
        initialization() {
            let scop = this
            scop.token = $cookies.get("Breaker")
            $cookies.remove("Breaker")
            scop.userInfo = scop.readJSONFromElement($('#data-userInfo'), 'data-userInfo') || {}
            console.log(scop.userInfo)
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

        addGoods() {
            let scop = this
            try {
                scop.isLoading = true
                const {canvas} = this.$refs.cropper.getResult();
                canvas.toBlob((blob) => {
                    scop.file = new File([blob], 'cropped-image.jpg', {type: 'image/jpeg'});
                    var form = new FormData();
                    form.append("commodity_name", scop.goods.name);
                    form.append("goods_type", scop.goods.type);
                    form.append("trademark", scop.goods.brand);
                    form.append("count", scop.goods.quantity);
                    form.append("price", scop.goods.price);
                    form.append("image_commodity", scop.file);
                    form.append("user", scop.userInfo.email);
                    form.append("description", scop.goods.description);

                    var settings = {
                        "url": "http://127.0.0.1:8000/api/commodities",
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
                        Swal.fire({
                            position: 'top-end',
                            icon: 'success',
                            title: 'Thêm sản phẩm thành công',
                            showConfirmButton: false,
                            timer: 1500
                        })
                        scop.isLoading = false
                    }).catch(err => {
                        alert(err)
                        scop.isLoading = true
                    });
                }, this.image.type);
            } catch (e) {
                scop.isLoading = false
                alert(e)
            }
        },
        reset() {
            this.image = {
                src: null,
                type: null,
            };
        },
        loadImage(event) {
            //define the width to resize e.g 600px
            var resize_width = 424;//without px
            // Reference to the DOM input element
            const {files} = event.target;
            // Ensure that you have a file before attempting to read it
            if (files && files[0]) {
                console.log(files[0], typeof files[0])
                // 1. Revoke the object URL, to allow the garbage collector to destroy the uploaded before file
                if (this.image.src) {
                    URL.revokeObjectURL(this.image.src);
                }
                // 2. Create the blob link to the file to optimize performance:
                const blob = URL.createObjectURL(files[0]);

                // 3. The steps below are designated to determine a file mime type to use it during the
                // getting of a cropped image from the canvas. You can replace it them by the following string,
                // but the type will be derived from the extension and it can lead to an incorrect result:
                //
                // this.image = {
                //    src: blob;
                //    type: files[0].type
                // }

                // Create a new FileReader to read this image binary data
                const reader = new FileReader();
                // Define a callback function to run, when FileReader finishes its job
                reader.onload = (e) => {
                    // Note: arrow function used here, so that "this.image" refers to the image of Vue component
                    this.image = {
                        // Read image as base64 and set it as src:
                        src: blob,
                        // Determine the image type to preserve it during the extracting the image from canvas:
                        type: getMimeType(e.target.result, files[0].type),
                    };
                };
                // Start the reader job - read file as a data url (base64 format)
                reader.readAsArrayBuffer(files[0]);
            }
        },
        onChange({coordinates, image}) {
            this.result = this.$refs.cropper.getResult().canvas.toDataURL();
        },
    },
    components: {
        Cropper: VueAdvancedCropper.Cropper,
        CircleStencil: VueAdvancedCropper.CircleStencil,
        Preview: VueAdvancedCropper.Preview
    },
    delimiters: ['[[', ']]'],
    destroyed() {
        // Revoke the object URL, to allow the garbage collector to destroy the uploaded before file
        if (this.image.src) {
            URL.revokeObjectURL(this.image.src);
        }
    },
}).mount('#warehouses');
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
const popover = new bootstrap.Popover('.popover-dismiss', {
    trigger: 'focus'
})