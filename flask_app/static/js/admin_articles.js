function searchArticles() {
    const query = document.getElementById('searchInput').value;

    fetch(`/admin/articles/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const articles = data.articles;
            const searchResultsDiv = document.getElementById('searchResults');
            searchResultsDiv.innerHTML = '';  // Clear previous results

            articles.forEach(article => {
                const articleBox = document.createElement('form');
                articleBox.method = "POST"
                articleBox.action = "/admin/articles/add"
                
                const articleData = {
                    'title': article.title,
                    'description': article.description,
                    'content': article.content,
                    'url': article.url,
                    'source_name': article.source.name,
                    'image': article.image,
                    'published_at': article.publishedAt,
                    'source_url': article.source.url,
                    'priority': 0
                };




                const imgDiv = document.createElement('div');
                imgDiv.className = "articles-img-box";
                const img = document.createElement('img');
                img.src = article.image;
                img.alt = "article image";
                imgDiv.appendChild(img);
                articleBox.appendChild(imgDiv);
            
                const infoDiv = document.createElement('div');
                infoDiv.className = "articles-info";
                const title = document.createElement('h1');
                title.textContent = article.title;
                const source = document.createElement('p');
                source.textContent = article.source.url;
                const publishedAt = document.createElement('p');
                publishedAt.textContent = article.publishedAt;
                infoDiv.appendChild(title);
                infoDiv.appendChild(source);
                infoDiv.appendChild(publishedAt);
                articleBox.appendChild(infoDiv);

                Object.keys(articleData).forEach(key => {
                    const input = document.createElement('input');
                    input.type = "hidden";
                    input.name = key;
                    input.value = articleData[key];
                    articleBox.appendChild(input);
                });
            
                const submitButton = document.createElement('button');
                submitButton.type = "submit";
                submitButton.textContent = "Submit";
            
                articleBox.appendChild(submitButton);
                searchResultsDiv.appendChild(articleBox);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}