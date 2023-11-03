
// 是否生成过代码
var isGenerated = false;

// 任务类型和模型列表,需要实时更新
var modelList = {
    "classification": ["LeNet", "ResNet18", "ResNet50", "MobileNet"],
    "detection": ["Yolov3", "SSD_Lite", "Faster-RCNN"],
}

var lossChart = echarts.init(document.getElementById('loss-chart'));
var accChart = echarts.init(document.getElementById('acc-chart'));

// 图表配置
var lossOption = {
    title: {
        text: 'Loss Chart'
    },
    tooltip: {},
    legend: {
        data: ['loss']
    },
    xAxis: {
        data: [],
        name: 'epoch',

    },
    yAxis: {
        name: 'loss',
    },
    series: [{
        name: 'loss',
        type: 'line',
        smooth: true,
        data: []
    }]
};

var accOption = {
    title: {
        text: 'Accuracy Chart'
    },
    tooltip: {},
    legend: {
        data: ['accuracy']
    },
    xAxis: {
        data: [],
        name: 'epoch',
    },
    yAxis: {
        name: 'accuracy',
    },
    series: [{
        name: 'accuracy',
        type: 'line',
        smooth: true,
        data: []
    }]
};



document.addEventListener('DOMContentLoaded', function () {

    // 选择任务类型
    document.getElementById('task-submit-btn').addEventListener('click', function () {
        // 获取选中的任务类型
        var selectedTask = document.getElementById('task-select').value;
        // 构建请求数据
        var requestData = {
            task: selectedTask
        };
        // 发送POST请求到Flask后端
        fetch('/mmedu/select_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
            .then(response => response.json())
            .then(data => {
                // 处理成功响应
                console.log(data);
                // 在这里可以执行其他操作，例如更新页面内容
            })
            .catch(error => {
                // 处理错误
                console.error(error);
            });
        updateCarouselContent(selectedTask, null, null);

        if (selectedTask == 'classification') {
            var modelSelect = document.getElementById('model-select');
            modelSelect.innerHTML = '';
            for (var i = 0; i < modelList['classification'].length; i++) {
                var option = document.createElement("option");
                option.text = modelList['classification'][i];
                option.value = modelList['classification'][i];
                modelSelect.appendChild(option);
            }
        }
        else if (selectedTask == 'detection') {
            var modelSelect = document.getElementById('model-select');
            modelSelect.innerHTML = '';
            for (var i = 0; i < modelList['detection'].length; i++) {
                var option = document.createElement("option");
                option.text = modelList['detection'][i];
                option.value = modelList['detection'][i];
                modelSelect.appendChild(option);
            }
        }
        // 现在，您可以在JavaScript代码中使用modelList
        console.log(modelList);


    });


});
// 选择模型
    document.getElementById('model-submit-btn').addEventListener('click', function () {
    // 获取选中的任务类型
    var selectedModel = document.getElementById('model-select').value;
    // 构建请求数据
    var requestData = {
        model: selectedModel
    };
    // 发送POST请求到Flask后端
    fetch('/mmedu/select_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });

    updateCarouselContent(null, selectedModel, null);

    });


// 更新轮播项的内容
function updateCarouselContent(task, model, dataset) {
    var carouselItems = document.querySelectorAll('.carousel-item');

    // 根据任务类型和模型来更新轮播项的内容
    for (var i = 0; i < carouselItems.length; i++) {
        if (i === 0) {
            // 第一个轮播项，根据任务类型更新内容
            if (task) {
                var subtitle = carouselItems[i].querySelector('.subtitle');
                subtitle.textContent = '当前选择的任务是：' + task;
                // reload the page
            }
        } else if (i === 1) {
            // 第二个轮播项，根据模型更新内容
            if (model) {
                var subtitle = carouselItems[i].querySelector('.subtitle');
                subtitle.textContent = '当前选择的模型是：' + model;
            }
        }
        else if (i === 2) {
            // 第三个轮播项，根据模型更新内容
            if (dataset) {
                var subtitle = carouselItems[i].querySelector('.subtitle');
                subtitle.textContent = '当前选择的数据集是：' + dataset;
            }
        }
    }
}

// 在页面渲染时，获取本地数据集
// 在跳转到第三个轮播项时，获取本地数据集

// 监听跳转到第三个页面：
$(document).ready(function () {
    $('#myCarousel').on('slid.bs.carousel', function () {
        var currentIndex = $('#myCarousel .active').index();
        if (currentIndex == 2) {
            fetch('/mmedu/get_local_dataset')
                .then(response => response.json())
                .then(data => {
                    // 处理成功响应
                    console.log(data);
                    // 在第三个轮播项中显示数据集列表
                    // 获取data中的key
                    var keys = Object.keys(data);
                    console.log(keys); // ["cls", "det"] 但是这里的key和任务不一致，一个是简写一个是全称
                    // 获取选中的任务类型
                    var selectedTask = document.getElementById('task-select').value;
                    var dataSetSelect = document.getElementById('dataset-select')
                    // 如果任务是分类，显示分类数据集列表
                    if (selectedTask == "classification") {
                        dataSetSelect.innerHTML = '';
                        for (var i = 0; i < data['cls'].length; i++) {
                            var option = document.createElement("option");
                            option.text = data['cls'][i];
                            option.value = data['cls'][i];
                            dataSetSelect.appendChild(option);
                        }
                    }
                    // 如果任务是检测，显示检测数据集列表
                    else if (selectedTask == "detection") {
                        dataSetSelect.innerHTML = '';
                        for (var i = 0; i < data['det'].length; i++) {
                            var option = document.createElement("option");
                            option.text = data['det'][i];
                            option.value = data['det'][i];
                            dataSetSelect.appendChild(option);
                        }
                    }
                })
                .catch(error => {
                    // 处理错误
                    console.error(error);
                });
        }

        else if (currentIndex == 0) {
            var selectedModel = document.getElementById('model-select').value;
            updateCarouselContent(null, selectedModel, null);
        }
        else if (currentIndex == 1) {
            var selectedTask = document.getElementById('task-select').value;
            updateCarouselContent(selectedTask, null, null);
        }
    });
});


// 选择数据集
document.getElementById('dataset-submit-btn').addEventListener('click', function () {
    // 获取选中的任务类型
    var selectedDataset = document.getElementById('dataset-select').value;
    // 构建请求数据
    var requestData = {
        dataset: selectedDataset
    };
    // 发送POST请求到Flask后端
    fetch('/mmedu/select_dataset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            // 在这里可以执行其他操作，例如更新页面内容
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });
    updateCarouselContent(null, null, selectedDataset);

});

// 点击生成代码
document.getElementById('code-generate-btn').addEventListener('click', function () {
    // 发送POST请求到Flask后端
    fetch('/mmedu/get_code', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            isGenerated = true;
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


// 表单提交
document.getElementById("train_cfg_form").addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch('/mmedu/set_base_cfg', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            // 在这里可以执行其他操作，例如更新页面内容

        })
        .catch(error => {
            // 处理错误
            console.error(error);
        })

});

// 获取id为cfgAdvanceSet div中的内容,并提交数据到后端
document.getElementById("advset-submit-btn").addEventListener("click", function (event) {
    event.preventDefault();
    var classNum = document.getElementById("classNum").value;
    var optimizerSelect = document.getElementById("optimizer-select");
    var optimizer = optimizerSelect.options[optimizerSelect.selectedIndex].value;
    var weightDecay = document.getElementById("weight-decay").value;
    var deviceSelect = document.getElementById("device-select");
    var device = deviceSelect.options[deviceSelect.selectedIndex].value;
    var pretrainedSelect = document.getElementById("pretrained-select");
    var pretrained = pretrainedSelect.options[pretrainedSelect.selectedIndex].value;

    var requestData = {
        "class_num": classNum,
        "optimizer": optimizer,
        "weight_decay": weightDecay,
        "device": device,
        "pretrained_model": pretrained
    };
    console.log(requestData);
    fetch('/mmedu/set_advance_cfg', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            // 在这里可以执行其他操作，例如更新页面内容
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });

});




// 函数：点击跳转到下一轮播项
function nextCarouselItem() {
    $('.carousel').carousel('next');
}

// 绑定到关闭按钮
document.getElementById('btn-modal-close').addEventListener('click', nextCarouselItem);
// document.getElementById('dataset-submit-btn').addEventListener('click', nextCarouselItem);
// document.getElementById('model-submit-btn').addEventListener('click', nextCarouselItem);


var total_log_data = [];

// 点击开始训练按钮，发送请求到后端
document.getElementById('start-train-btn').addEventListener('click', function () {
    if (!isGenerated) {
        alert("请先生成代码!");
        return;
    }
    get_epoch();
    // 构建请求数据
    // 发送POST请求到Flask后端
    fetch('/mmedu/start_thread', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    
    // 按钮被禁用
    document.getElementById('start-train-btn').disabled = true;

    clearTrainProgressBar();
    poll_log();
});

// 点击结束训练按钮，发送请求到后端
document.getElementById('stop-train-btn').addEventListener('click', function () {
    fetch('/mmedu/stop_thread', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // 训练按钮被启用
        document.getElementById('start-train-btn').disabled = false;

        // 停止轮询
        // clearInterval(intervalId);
        lossChart.hideLoading();
        accChart.hideLoading();
        if(data.success){
            $('#trainTerminateModal').modal('show');
        }
        else{
            trainTerminateModal = document.getElementById('trainTerminateModal');
            body = trainTerminateModal.getElementsByClassName("modal-body")[0];
            p = body.getElementsByTagName("p")[0];
            p.innerHTML = data.message;
            // 设置自动换行
            p.style.wordWrap = "break-word";
            $('#trainTerminateModal').modal('show');
        }
    });
});




// 轮询线程状态
function pollThreadStatus() {
    fetch('/mmedu/get_message', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            // 处理成功响应
            console.log(data);
            // 如果跟上一次的数据不一致，就加入
            if (total_log_data.length == 0 || total_log_data[total_log_data.length - 1] != data) {
                total_log_data.push(data);
            }
        })
        .catch(error => {
            // 处理错误
            console.error(error);
        });
}



var G_totalEpoch = 0;
var G_checkpoints_path = "";

function get_epoch(){
    // 从后端获取总epoch
    fetch('/mmedu/get_epoch', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        G_totalEpoch = data['epoch'];
    });
}




function get_checkpoints_path(){

    var checkpoints_path = "";
    // 从后端获取checkpoints_path
    fetch('/mmedu/get_checkpoints_path', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        checkpoints_path = data['checkpoints_path'];
        setTrainFinishModal(checkpoints_path);
    }
    );

    return checkpoints_path;
}



// console.log(G_checkpoints_path);
const socket = io.connect('http://localhost:5000');
function poll_log(){
// 连接socket

    lossList = []
    accList = []
    currentEpoch = 1
    temp_loss = [];

    // 清除图表数据
    lossOption.series[0].data = [];
    accOption.series[0].data = [];

    // chart的加载动画
    lossChart.showLoading();
    accChart.showLoading();

    flag = true;
socket.on('log', (log) => {
    // console.log(log);
    if(flag){
        lossChart.hideLoading();
        accChart.hideLoading();
        // 显示图表的坐标轴
        lossChart.setOption(lossOption);
        accChart.setOption(accOption);
        flag = false;
    }



    // 如果跟上一次的数据不一致，就加入
    if (total_log_data.length == 0 || total_log_data[total_log_data.length - 1] != log) {
        total_log_data.push(log);
        logJsno = JSON.parse(log);

        epoch = logJsno['epoch'];
        mode = logJsno['mode'];
        loss = logJsno['loss'];
        acc = logJsno['accuracy_top-1'];
        if (mode == "train" && epoch==currentEpoch){
            temp_loss.push(loss);
            console.log(loss)
        }
        else if (mode=="val" && epoch==currentEpoch){
            accList.push(acc)
            console.log("accList",acc);
            console.log("temp_loss",temp_loss);
            // 求temp_loss的平均值
            var sum = 0;
            for (var i=0;i<temp_loss.length;i++){
                sum += temp_loss[i];
            }
            var avgLoss = sum/temp_loss.length;
            // 设置进度条
            setTrainProgressBar(epoch);
            // 更新图表
            lossOption.series[0].data.push(avgLoss);
            lossChart.setOption(lossOption);
            accOption.series[0].data.push(acc);
            accChart.setOption(accOption);

            console.log("avgloss",avgLoss);
            // 清空temp_loss
            temp_loss = [];
            lossList.push(avgLoss);
            currentEpoch+=1
        }

        if (mode == "val" && epoch==G_totalEpoch){ // 这段代码逻辑有点问题，其实不应该发请求
            console.log("应该停止训练模型了");
            fetch('/mmedu/stop_thread', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                console.log(lossList);
                console.log(accList);
                // 清空lossList,accList
                lossList = [];
                accList = [];
                currentEpoch = 1;
                get_checkpoints_path();
                invervalEpoch = Math.floor(G_totalEpoch/10);
                // 最后绘制图表的x轴
                lossOption.xAxis.data = [];
                accOption.xAxis.data = [];
                for (var i=1;i<=G_totalEpoch;i++){
                    if (i%invervalEpoch==0){
                        lossOption.xAxis.data.push(i.toString());
                        accOption.xAxis.data.push(i.toString());
                    }
                }
                lossChart.setOption(lossOption);
                accChart.setOption(accOption);
                // 训练按钮被启用
                document.getElementById('start-train-btn').disabled = false;

                
            });
        }

    }
})
}



function setTrainProgressBar(epoch){
    var percent = epoch/G_totalEpoch*100;
    var progressBar = document.getElementById('progress-bar');
    progressBar.setAttribute("aria-valuenow",percent.toString());
    progressBar.style.width = percent.toString()+"%";
}

function clearTrainProgressBar(){
    var progressBar = document.getElementById('progress-bar');
    progressBar.setAttribute("aria-valuenow","0");
    progressBar.style.width = "0%";
}

function setTrainFinishModal(checkpoints_path){
    console.log("setTrainFinishModal");
    var trainFinishModal = document.getElementById('trainFinishModal');
    trainFinishModal.setAttribute("aria-labelledby","Train Finish");
    body = trainFinishModal.getElementsByClassName("modal-body")[0];
    p = body.getElementsByTagName("p")[0];
    p.innerHTML = "训练已经结束，模型权重和日志保存路径为:"+checkpoints_path;
    // 设置自动换行
    p.style.wordWrap = "break-word";
    $('#trainFinishModal').modal('show');
}


// const steps = document.querySelectorAll('.step');

// steps.forEach((step, index) => {
//   step.addEventListener('click', () => {
//     // 移除先前高亮的步骤
//     document.querySelector('.step.active')?.classList.remove('active');
//     // 高亮当前点击的步骤
//     step.classList.add('active');
//   });
// });


// 当点击设置其他参数
document.getElementById('set-other-params-btn').addEventListener('click', function () {
    fetch('/mmedu/get_local_pretrained_model', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        // 将data中的模型列表添加到select中
        var pretrainedModelSelect = document.getElementById('pretrained-select');
        pretrainedModelSelect.innerHTML = '';
        var option_none = document.createElement("option");
        option_none.text = "不使用";
        option_none.value = "None";
        pretrainedModelSelect.appendChild(option_none);
        for (var i = 0; i < data.length; i++) {
            var option = document.createElement("option");
            option.text = data[i];
            option.value = data[i];
            pretrainedModelSelect.appendChild(option);
        }
    })
});
