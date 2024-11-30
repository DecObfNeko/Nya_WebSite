  function logout() {
        // 删除名为 'MiaoWu' 的 cookie
        document.cookie = 'MiaoWu=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        // 刷新页面
        location.reload();
    }
  function copyIP() {
        // 假设你想复制一个特定的 IP 地址，请用实际的 IP 替换 'yourIpAddress'
        var ipAddress = 'mc.nyacat.cloud';

        // 创建一个临时的 textarea 元素
        var textarea = document.createElement('textarea');
        textarea.value = ipAddress;

        // 将 textarea 添加到文档中
        document.body.appendChild(textarea);

        // 选择 textarea 中的文本
        textarea.select();

        // 将选定的文本复制到剪贴板
        document.execCommand('copy');

        // 移除临时的 textarea
        document.body.removeChild(textarea);

        // 将 <span> 中的文本更改为 "成功复制"，并添加渐入效果的类
        var copySpan = document.querySelector('.btn-get-started span');
        copySpan.textContent = 'Replicated Successfully';
        copySpan.classList.add('copy-success');

        // 异步更新样式以触发渐入效果
        setTimeout(function () {
            // 添加渐出效果的类
            copySpan.classList.add('copy-fade');
        }, 0);

        // 使用 setTimeout 在过渡后重置文本并移除类
        setTimeout(function () {
            copySpan.textContent = 'Copy IP';
            copySpan.classList.remove('copy-success', 'copy-fade');
        }, 500); // 根据过渡的持续时间调整超时时间
    }