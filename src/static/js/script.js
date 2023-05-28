// // Função para enviar o formulário e exibir o resultado
// function enviarFormulario(event) {
//     event.preventDefault();

//     var videoLink = document.getElementById('video-link').value;

//     // Fazer uma requisição AJAX ao endpoint /analisar
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', '/analisar', true);
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

//     xhr.onreadystatechange = function () {
//         if (xhr.readyState === 4) {
//             if (xhr.status === 200) {
//                 var response = JSON.parse(xhr.responseText);
//                 if (response.error) {
//                     exibirErro(response.error);
//                 } else {
//                     exibirResultado(response);
//                 }
//             } else {
//                 exibirErro('Ocorreu um erro durante a análise. Por favor, tente novamente mais tarde.');
//             }
//         }
//     };

//     var formData = new FormData();
//     formData.append('video_link', videoLink);

//     xhr.send(formData);
// }

// // Função para exibir o resultado da análise na página
// function exibirResultado(data) {
//     var resultContainer = document.getElementById('result-container');
//     resultContainer.innerHTML = '';

//     // Exibir a média de sentimento
//     var averageScore = document.createElement('h2');
//     averageScore.textContent = 'Média de Sentimento: ' + data.average_score;
//     resultContainer.appendChild(averageScore);

//     // Exibir o percentual de comentários positivos e negativos
//     var sentimentContainer = document.createElement('div');
//     sentimentContainer.className = 'sentiment';
//     var positivePercentage = document.createElement('p');
//     positivePercentage.textContent = data.positive_percentage + '% Positivos';
//     var negativePercentage = document.createElement('p');
//     negativePercentage.textContent = data.negative_percentage + '% Negativos';
//     sentimentContainer.appendChild(positivePercentage);
//     sentimentContainer.appendChild(negativePercentage);
//     resultContainer.appendChild(sentimentContainer);

//     // Exibir os comentários analisados
//     var commentsContainer = document.createElement('div');
//     commentsContainer.className = 'comments';
//     var commentsHeader = document.createElement('h3');
//     commentsHeader.textContent = 'Comentários Analisados';
//     commentsContainer.appendChild(commentsHeader);
//     var commentsList = document.createElement('ul');
//     data.comments.forEach(function (comment) {
//         var commentItem = document.createElement('li');
//         commentItem.innerHTML = '<strong>' + comment.author + '</strong> - ' + comment.sentiment + ': ' + comment.text;
//         commentsList.appendChild(commentItem);
//     });
//     commentsContainer.appendChild(commentsList);
//     resultContainer.appendChild(commentsContainer);
// }

// // Função para exibir mensagens de erro
// function exibirErro(error) {
//     var resultContainer = document.getElementById('result-container');
//     resultContainer.innerHTML = '';

//     var errorParagraph = document.createElement('p');
//     errorParagraph.textContent = error;

//     resultContainer.appendChild(errorParagraph);
// }

// // Vincular o evento de envio do formulário à função enviarFormulario
// var form = document.getElementById('my-form');
// form.addEventListener('submit', enviarFormulario);
