document.addEventListener('DOMContentLoaded', () => {
    cargarPosts();
});

async function cargarPosts() {
    const contenedor = document.getElementById('contenedor-posts');
    
    const token = localStorage.getItem('access_token');
    
// esto es pa obligar a iniciar sesion, quitar d comentario dsp, es solo pa probarlo
//    if (!token) {
//        alert("¡Debes iniciar sesión primero (o_O) !");
//        window.location.href = "index.html";
//        return;
//    }
    
//cambiar link dsp tmb
    try {
        const respuesta = await fetch('http://127.0.0.1:8000/api/posts/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, 
                'Content-Type': 'application/json'
            }
        });

        if (respuesta.ok) {
            const posts = await respuesta.json();
            
            if (posts.length === 0) {
                contenedor.innerHTML = "<p style='text-align:center;'>Aún no hay gatitos aquí. ¡Sé el primero en publicar!</p>";
                return;
            }

            posts.forEach(post => {
                const tarjetaHTML = `
                <article class="post-card">
                    <header class="post-header">
                        <div class="user-info">
                            <div class="user-details">
                                <h4>${post.cat}</h4> <p>@usuario_gatuno</p>
                            </div>
                        </div>
                        <span class="post-time">${new Date(post.created_at).toLocaleDateString()}</span>
                    </header>

                    <div class="post-image-container">
                        <img src="${post.image}" alt="Foto del post" class="post-image">
                    </div>

                    <div class="post-actions">
                        <span class="action-btn">♡ ${post.likes}</span>
                    </div>

                    <div class="post-caption">
                        <p>${post.caption}</p>
                    </div>
                </article>
                `;
                
                contenedor.innerHTML += tarjetaHTML;
            });

        } else {
            console.error("No se pudieron cargar los posts");
        }

    } catch (error) {
        console.error("Error de conexión:", error);
        contenedor.innerHTML = "<p style='text-align:center; color:red;'>No pudimos conectar con la gatería :(</p>";
    }
}
// nvo post

const imageInput = document.getElementById('image-input');
const fileNameSpan = document.getElementById('file-name');
const submitPostBtn = document.getElementById('submit-post-btn');
const captionInput = document.getElementById('caption-input');

imageInput.addEventListener('change', () => {
    if (imageInput.files.length > 0) {
        fileNameSpan.textContent = imageInput.files[0].name;
    } else {
        fileNameSpan.textContent = "Ninguna foto seleccionada";
    }
});

submitPostBtn.addEventListener('click', async () => {
    const token = localStorage.getItem('access_token');
    const comentarioTexto = captionInput.value.trim();
    const archivoFoto = imageInput.files[0];

    if (!archivoFoto) {
        alert("¡Por favor selecciona una foto de tu gatito primero! ^•⩊•^");
        return;
    }

    const formData = new FormData();
    formData.append('caption', comentarioTexto);
    formData.append('image', archivoFoto); 

    try {
        submitPostBtn.disabled = true;
        submitPostBtn.textContent = "Subiendo...ᓚᘏᗢ";

      // el link d aquí se debería cambiar por el q corresponda, este es local nda mas,creo
        const respuesta = await fetch('http://127.0.0.1:8000/api/posts/', {  
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (respuesta.ok) {
            alert("¡Post felino publicado con éxito! ᓚᘏᗢ");
            
            captionInput.value = "";
            imageInput.value = "";
            fileNameSpan.textContent = "Ninguna foto seleccionada";
            
            document.getElementById('contenedor-posts').innerHTML = "";
            cargarPosts();
        } else {
            alert("Hubo un problema al subir el post. Revisa los formatos.");
        }

    } catch (error) {
        console.error("Error al publicar:", error);
        alert("Error de conexión con el servidor de los gatitos.");
    } finally {
        submitPostBtn.disabled = false;
        submitPostBtn.textContent = "Publicar ᓚᘏᗢ";
    }
});
