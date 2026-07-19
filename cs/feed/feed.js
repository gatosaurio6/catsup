// login
const modalLogin = document.getElementById('modal-login');
const btnAbrirLogin = document.getElementById('btn-abrir-login');
const btnCerrarLogin = document.getElementById('btn-cerrar-login');

btnAbrirLogin.addEventListener('click', () => {
    modalLogin.style.display = 'block';
});

btnCerrarLogin.addEventListener('click', () => {
    modalLogin.style.display = 'none';
});

// iniciar
const usernameInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');
const loginBtn = document.getElementById('login-btn');

loginBtn.addEventListener('click', async () => {
    const datosUsuario = {
        username: usernameInput.value,
        password: passwordInput.value
    };

    try {
        const respuesta = await fetch('https://catsup.servemp3.com/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datosUsuario)
        });

        if (respuesta.ok) {
            const resultado = await respuesta.json();
            localStorage.setItem('access_token', resultado.access);
            alert("¡Bienvenido a Catsup.com! ᓚᘏᗢ");
            
            modalLogin.style.display = 'none';
            cargarPosts(); 
        } else {
            alert("Error: Revisa tu usuario o contraseña.");
        }
    } catch (error) {
        console.error("Error al conectar:", error);
    }
});

//cargar 
async function cargarPosts() {
    const contenedor = document.getElementById('contenedor-posts');
    contenedor.innerHTML = "";
    
    try {
        const respuesta = await fetch('https://catsup.servemp3.com/api/posts/', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
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
                                <h4>Usuario ${post.ID_usuario || 'Gatuno'}</h4> <p>@usuario_gatuno</p>
                            </div>
                        </div>
                        <span class="post-time">${new Date(post.fecha_publicacion).toLocaleDateString()}</span>
                    </header>

                    <div class="post-image-container">
                        <img src="${post.url_multimedia}" alt="Foto del post" class="post-image">
                    </div>

                    <div class="post-actions">
                        <span class="action-btn" data-post-id="${post.ID || post.id}" style="cursor: pointer;">♡ ${post.likes || 0}</span>
                    </div>

                    <div class="post-caption">
                        <p>${post.titulo}</p>
                    </div>

                    <div class="seccion-comentarios">
                        <button class="btn-ver-comentarios" data-post-id="${post.ID || post.id}">Ver comentarios</button>
                        
                        <div class="lista-comentarios" id="lista-comentarios-${post.ID || post.id}" style="display: none; margin-top: 10px; border-top: 1px solid #eee; padding-top: 10px;">
                        </div>
                        
                        <div class="escribir-comentario" style="margin-top: 10px; display: flex; gap: 5px;">
                            <input type="text" id="input-comentario-${post.ID || post.id}" placeholder="Escribe algo bonito..." style="flex-grow: 1; padding: 5px; border-radius: 5px; border: 1px solid #ccc;">
                            <button class="btn-enviar-comentario" data-post-id="${post.ID || post.id}" style="padding: 5px 10px; border-radius: 5px; background-color: #ffb6c1; border: none; cursor: pointer;">Enviar</button>
                        </div>
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

//new postttt
const imageInput = document.getElementById('image-input');
const fileNameSpan = document.getElementById('file-name');
const submitPostBtn = document.getElementById('submit-post-btn');
const captionInput = document.getElementById('caption-input');

if (imageInput) {
    imageInput.addEventListener('change', () => {
        if (imageInput.files.length > 0) {
            fileNameSpan.textContent = imageInput.files[0].name;
        } else {
            fileNameSpan.textContent = "Ninguna foto seleccionada";
        }
    });
}

submitPostBtn.addEventListener('click', async () => {
    const token = localStorage.getItem('access_token');
    
    // validar
    if (!token) {
        alert("¡Debes iniciar sesión para publicar fotos de gatitos!");
        modalLogin.style.display = 'block';
        return;
    }

    const comentarioTexto = captionInput.value.trim();
    const archivoFoto = imageInput.files[0];

    if (!archivoFoto) {
        alert("¡Por favor selecciona una foto de tu gatito primero! ^•⩊•^");
        return;
    }

    const formData = new FormData();
    formData.append('titulo', comentarioTexto);
    formData.append('url_multimedia', archivoFoto); 

    try {
        submitPostBtn.disabled = true;
        submitPostBtn.textContent = "Subiendo...ᓚᘏᗢ";

        const respuesta = await fetch('https://catsup.servemp3.com/api/posts/', {  
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

//coments y cosaas
document.getElementById('contenedor-posts').addEventListener('click', async (e) => {
    const token = localStorage.getItem('access_token');
    const modalLogin = document.getElementById('modal-login');    
    
    // like/enviar
    if (e.target.classList.contains('btn-enviar-comentario') || e.target.classList.contains('action-btn')) {
        if (!token) {
            alert("¡Debes iniciar sesión para interactuar con los gatitos! 🐾");
            modalLogin.style.display = 'block';
            return; 
        }
    }

    // ver ocment
    if (e.target.classList.contains('btn-ver-comentarios')) {
        const postId = e.target.getAttribute('data-post-id');
        const contenedorComentarios = document.getElementById(`lista-comentarios-${postId}`);
        
        if (contenedorComentarios.style.display === 'none') {
            contenedorComentarios.style.display = 'block';
            contenedorComentarios.innerHTML = '<p>Cargando... ᓚᘏᗢ </p>';
            
            try {
                const respuesta = await fetch(`https://catsup.servemp3.com/api/comentarios/post/${postId}/`);
                
                if (respuesta.ok) {
                    const data = await respuesta.json();
                    contenedorComentarios.innerHTML = ''; 
                    
                    if (data.comments.length === 0) {
                        contenedorComentarios.innerHTML = '<p style="font-size: 0.9em; color: gray;">Sé el primero en comentar :3</p>';
                    } else {
                        data.comments.forEach(c => {
                            contenedorComentarios.innerHTML += `
                                <div style="margin-bottom: 8px; font-size: 0.9em;">
                                    <strong>Usuario ${c.ID_usuario}:</strong> <span>${c.contenido}</span>
                                </div>
                            `;
                        });
                    }
                }
            } catch (error) {
                contenedorComentarios.innerHTML = '<p>Error al cargar /ᐠ｡ꞈ｡ᐟ\\</p>';
            }
        } else {
            contenedorComentarios.style.display = 'none'; 
        }
    }

    // enviar coment
    if (e.target.classList.contains('btn-enviar-comentario')) {
        const postId = e.target.getAttribute('data-post-id');
        const inputElement = document.getElementById(`input-comentario-${postId}`);
        const contenido = inputElement.value.trim();
        
        if (!contenido) return; 

        e.target.disabled = true;
        e.target.textContent = '...';

        try {
            const respuesta = await fetch('https://catsup.servemp3.com/api/comentarios/comentar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    ID_post: postId,
                    contenido: contenido,
                    ID_usuario: localStorage.getItem('user_id') || 1
                })
            });

            if (respuesta.ok) {
                inputElement.value = '';
                alert('¡Comentario publicado! ᓚᘏᗢ');
            } else {
                alert('Hubo un problema al comentar :(');
            }
        } catch (error) {
            console.error("Error al enviar comentario:", error);
        } finally {
            e.target.disabled = false;
            e.target.textContent = 'Enviar';
        }
    }
    // likeeeeeeeeeee
    if (e.target.classList.contains('action-btn')) {
        const postId = e.target.getAttribute('data-post-id');
        
        try {
            const respuesta = await fetch('https://catsup.servemp3.com/api/ranking/rv/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` 
                },
                body: JSON.stringify({
                    id_post: postId,
                    accion: "like" 
                })
            });

            if (respuesta.ok) {
                let textoActual = e.target.textContent;
                let likesActuales = parseInt(textoActual.replace(/[^0-9]/g, '')) || 0; 
                
                if (respuesta.status === 201 || respuesta.status === 200) {
                    e.target.textContent = `♥ ${likesActuales + 1}`;
                    e.target.style.color = '#ff6bc9'; 
                    e.target.style.fontWeight = 'bold';
                } else if (respuesta.status === 204) {
                    e.target.textContent = `♡ ${Math.max(0, likesActuales - 1)}`;
                    e.target.style.color = 'black'; 
                    e.target.style.fontWeight = 'normal';
                }
            } else {
                console.error("não não amigão: Error al registrar el voto");
            }
        } catch (error) {
            console.error("Fallo de conexión al dar like:", error);
        }
    }
});

cargarPosts();