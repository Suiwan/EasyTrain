document.addEventListener("DOMContentLoaded", function() {
    const addLayerButton = document.getElementById("addLayer");
    addLayerButton.addEventListener("click", addLayer);

    let lineList = [];

    let previousOutputSize = 0;


    function addLayer() {
        // 添加新层
        const network = document.querySelector(".network");
        const existingLayers = network.querySelectorAll(".layer");
        // console.log(existingLayers.length);
        newLayer = createLayer(existingLayers.length + 1);
        network.appendChild(newLayer);

        const nowLayerLength = existingLayers.length + 1;

        if (nowLayerLength == 1){
            // 如果是第一层，添加监听器以更新上一层的输出维度
            const firstOutput = document.getElementById(`output-size${nowLayerLength}`);
            firstOutput.addEventListener("input", function() {
                const firstoutputSize = parseInt(firstOutput.value);
                if(!isNaN(firstoutputSize)){
                    previousOutputSize = firstoutputSize;
                }
            });
        }
        else if(nowLayerLength > 1){
            // 对于后续层，为输出维度添加监听以更新输入维度
            for (let i = 1; i< nowLayerLength;i++){
                const output = document.getElementById(`output-size${i}`);
                const input = document.getElementById(`input-size${i+1}`);
                output.addEventListener("input", () => {
                    const currentOutput = document.getElementById(`output-size${i}`);
                    const outputSize = parseInt(currentOutput.value);
                    if (!isNaN(outputSize)){
                        input.value = outputSize;
                    }
            });
        }

        // 为最后一层添加监听器，以更新输出维度
        const lastOutput = document.getElementById(`output-size${nowLayerLength}`);
        lastOutput.addEventListener("input", function() {
            const lastoutputSize = parseInt(lastOutput.value);
            if(!isNaN(lastoutputSize)){
                previousOutputSize = lastoutputSize;
            }
        });
        }

        // 重新绘制线
        if (nowLayerLength > 1){
            // 先将之前的线删除
            for (let i = 0; i < lineList.length; i++) {
                lineList[i].remove();
            }
            lineList = [];
            // 重新绘制线
            for (let i = 0; i < nowLayerLength-1; i++) {
                line = createLine(document.getElementById(`layer-${i+1}`),document.getElementById(`layer-${i+2}`))
                lineList.push(line);
            }
        }
    }

    
    function createLine(layer1, layer2) {
        const line = new LeaderLine(layer1, layer2,{color:"white",dash:{animation:true}});
        line.setOptions({ startSocket: 'right', endSocket: 'left'});
        line.path = 'grid';
        return line;
    }


    function createLayer(layerNumber) {
        const layer = document.createElement("div");
        layer.className = "layer";
        layer.id = `layer-${layerNumber}`;
        
        const layerInfo = document.createElement("div");
        layerInfo.className = "layer-info";
        layerInfo.innerHTML = `
            <span class="layer-number">Layer #${layerNumber}</span>
            <span class="layer-type">类型：Linear</span>
        `;

        
        const layerDimensions = document.createElement("div");
        layerDimensions.className = "layer-dimensions";
        layerDimensions.innerHTML = `
        <span class="layer-name">输入维度:</span>
            <input type="text"  id="input-size${layerNumber}" value="${previousOutputSize}">
            <span class="layer-name">输出维度:</span>
            <input type="text"  id="output-size${layerNumber}" value="0">
        `;
        
        const activationDropdown = document.createElement("div");
        activationDropdown.className = "activation-dropdown";
        activationDropdown.innerHTML = `<span class="layer-name">激活函数:</span>
            <select>
                <option value="relu">ReLU</option>

                <option value="softmax">Softmax</option>
            </select>
        `;
        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-button";
        // deleteButton.classList.add("btn");
        // deleteButton.classList.add("btn-outline-danger");
        deleteButton.textContent = "x";
        // const deleteButton = document.createElement("img");
        // deleteButton.className = "delete-button";


        deleteButton.addEventListener("click", removeLayer);
        layer.appendChild(layerInfo);
        layer.appendChild(layerDimensions);
        layer.appendChild(activationDropdown);
        layer.appendChild(deleteButton);
        return layer;
    }


    function removeLayer(event) {
        // 删除当前层
        const layer = event.target.parentNode;
        // 删除线
        const layerId = layer.id;
        const layerNumber = layerId.split("-")[1];

        layer.classList.add("deleting");
        layer.parentNode.removeChild(layer);
        // 重新编号
        const layers = document.querySelectorAll(".layer");
        // console.log(layers);
        console.log(layers.length);
        for (let i = 0; i < layers.length; i++) {
            const layer = layers[i];
            const layerNumber = layer.querySelector(".layer-number");
            layerNumber.textContent = `Layer #${i + 1}`;
            layer.id = `layer-${i + 1}`;
        }

        // 重新绘制线
        // 先将之前的线删除
        for (let i = 0; i < lineList.length; i++) {
            lineList[i].remove();
        }
        lineList = [];
        // 重新绘制线
        for (let i = 0; i < layers.length-1; i++) {
            line = createLine(document.getElementById(`layer-${i+1}`),document.getElementById(`layer-${i+2}`))
            lineList.push(line);
        }
      }

    // 当层数过多时，滑动过程中会出现线的断裂，有些线需要隐藏，有些线需要显示
    var myNetwork = document.querySelector(".network-container");
    myNetwork.addEventListener("scroll", function() {
        for (let i = 0; i < lineList.length; i++) {
            lineList[i].position();
        }
    });

    // 当轮播到其他页面或者跳转到别的页面，线需要隐藏，当轮播到当前页面时，线需要显示
    function showLine() {
        for (let i = 0; i < lineList.length; i++) {
            lineList[i].show(['draw']);
        }
    }

    function hideLine() {
        for (let i = 0; i < lineList.length; i++) {
            lineList[i].hide(['fade',[{duration: 10}]]);
        }
    }

    // 跳转到其他页面时候隐藏线
    $(document).ready(function(){
        $('#myCarousel').on('slid.bs.carousel', function () {
            var currentIndex = $('#myCarousel .active').index();
            if(currentIndex == 1){
                showLine();
            }
            else{
                hideLine();
            }
    });
    });


      // 算法1：通过监听滚动事件，获取滚动条的位置，当滚动条的位置大于某个值时，隐藏线
      // 如果向下滚动，每滚动80px，从上往下隐藏一条线，如果向上滚动，每滚动80px，从下往上隐藏一条线
        // var scrollPos = 0;
        // var networkContainer = document.querySelector(".network-container");
        // networkContainer.addEventListener("scroll", function(){
        // var currentScrollPos = networkContainer.scrollTop;
        // console.log(currentScrollPos);
        // if (currentScrollPos > scrollPos){
        //     // 向下滚动
        //     num = parseInt(currentScrollPos/80);
        //     for (let i = 0; i < num; i++) {
        //         lineList[i].hide(['draw']);
        //     }
        //     for (let i = 0; i < lineList.length-num; i++) {
        //         lineList[lineList.length-1-i].show(['draw']);
        //     }
        //     scrollPos = currentScrollPos;
        // }
        // else{ // todo 微调一下算法，这块也可以不加，因为下方的线不是很妨碍观感。 网络搭建基本完成-10.31
        //     num = parseInt((scrollPos - currentScrollPos)/80);
        //     for (let i = 0; i < num; i++) {
        //         lineList[i].show(['draw']);
        //     }
        // }
        // });

    // 算法2：通过监听每一层的位置，当某一层的位置大于某个值时，隐藏线
    // 获得容器的高度
    var networkContainer = document.querySelector(".network-container");
    // 监听滚动事件
    networkContainer.addEventListener("scroll", function(){
        var networkTop = networkContainer.offsetTop;
        var networkHeight = networkContainer.offsetHeight;
        var networkBottom = networkTop + networkHeight;
        console.log(networkTop);
        console.log(networkBottom);
        // 获得每一层的高度
        var layers = document.querySelectorAll(".layer");
        var layerTop = [];
        var layerBottom = [];
        for (let i = 0; i < layers.length; i++) {
            layerTop.push(layers[i].offsetTop);
            layerBottom.push(layers[i].offsetTop + layers[i].offsetHeight);
        }
        console.log(layerTop);
        console.log(layerBottom);

        var currentScrollPos = networkContainer.scrollTop;
        console.log(currentScrollPos);
        for (let i = 0; i < layers.length-1; i++) {
            if (layerTop[i] > currentScrollPos && layerTop[i] < currentScrollPos + networkHeight){
                lineList[i].show(['draw']);
            }
            else{
                lineList[i].hide(['draw']);
            }
        }
    });

    // 鼠标悬停到删除按钮上时，删除按钮变红
    $(".delete-button").mouseover(function(){
        $(this).css("color","red");
    });

    // 监听提交按钮，提交网络结构到后盾
    const submitButton = document.getElementById("network-submit-btn");
    submitButton.addEventListener("click", submitNetwork);

    function submitNetwork(){
        // 获得所有层的信息
        const layers = document.querySelectorAll(".layer");
        const layerInfoList = [];
        let layerInfo = {};
        for (let i = 0; i < layers.length; i++) {
            const layer = layers[i];
            const id = i+1;
            const type = "linear"
            const inputSize = layer.querySelector(`#input-size${i+1}`).value;
            const outputSize = layer.querySelector(`#output-size${i+1}`).value;
            const activation = layer.querySelector(".activation-dropdown select").value;
            layerInfo = {
                "id": id,
                "type": type,
                "inputSize": inputSize,
                "outputSize": outputSize,
                "activation": activation
            };
            layerInfoList.push(layerInfo);
        }

        fetch("/basenn/set_network", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                network: layerInfoList
            })
        }).then(response => response.json())
        .then(result => {
            console.log(result);
            if (result.success){
                // 跳转到下一轮播页面
                $('#myCarousel').carousel('next');

            }
            else{
                alert("网络结构设置失败，请检查网络结构是否正确！");
            }
        });
    }



    // 设置训练参数

    // 表单提交
    document.getElementById("train_cfg_form").addEventListener("submit", function (event) {
        event.preventDefault();

        var formData = new FormData(this);

        // todo：参数检查
        fetch('/basenn/set_base_cfg', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在这里可以执行其他操作，例如更新页面内容
                // 显示模态框
                if(data.success){
                    $('#myModal3').modal('show');
                }
                else{
                    alert("参数设置失败，请检查参数是否正确！");
                }
                
            })
            .catch(error => {
                // 处理错误
                console.error(error);
            })

    });

    // 提交其他参数到后端
    document.getElementById("advset-submit-btn").addEventListener("click", function (event) {
            event.preventDefault();
            var metricsSelect = document.getElementById("metrics-select");
            var metrics = metricsSelect.options[metricsSelect.selectedIndex].value;
            var lossSelect = document.getElementById("loss-select");
            var loss = lossSelect.options[lossSelect.selectedIndex].value;
            var pretrainedSelect = document.getElementById("pretrained-select");
            var pretrained = pretrainedSelect.options[pretrainedSelect.selectedIndex].value;

            var requestData = {
                "metrics": metrics,
                "loss": loss,
                "pretrained": pretrained
            };
            console.log(requestData);
            fetch('/basenn/set_advance_cfg', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            }).then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.success){
                    // 跳转到下一轮播页面
                    // $('#myCarousel').carousel('next');
                }
                else{
                    alert("参数设置失败，请检查参数是否正确！");
                }
            });
    });



    // 点击生成代码
    document.getElementById('code-generate-btn').addEventListener('click', function () {
        // 发送POST请求到Flask后端
        fetch('/basenn/get_code', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在code标签中显示代码
                var code = document.getElementsByTagName('code')[0];
                code.innerHTML = data;
                // 渲染高亮
                hljs.highlightBlock(code);
            })
            .catch(error => {
                // 处理错误
                console.error(error);
            });
    });

    // 点击复制代码到剪贴板
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    function copyCode2Clipboard(){
        var clipboard = new ClipboardJS('#code-copy-btn');
        
        var clipbtn  = document.getElementById('code-copy-btn');

        clipboard.on('success', function(e) {
            // alert("代码已经复制到剪贴板!");
            e.clearSelection();
            // clipbtn.setAttribute('title','copy to clipboard');
            $('#code-copy-btn').tooltip('show')

            setTimeout(function(){
                $('#code-copy-btn').tooltip('hide')
            },1000);


        });
    }

    copyCode2Clipboard();


});
