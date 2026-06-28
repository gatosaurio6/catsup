document.addEventListener('DOMContentLoaded', () => {
    obtenerRanking();
});

async function obtenerRanking() {
    const contenedor = document.getElementById('podio-ganadores');
    const token = localStorage.getItem('access_token');

// bloque d prueba, estas lineas son solo de prueba, eliminar al conectar cn el resto
    const topGatosFalsos = [
        { cat: "Nini", caption: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ", likes: 512 },
        { cat: "Charol", caption: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ", likes: 284 },
        { cat: "Gato", caption: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ", likes: 120 }
    ];
    
    dibujarPodio(topGatosFalsos);
    return; 
// bloque d prueba 


// este si conecta cn el back
    try {
        //cambiar url x la real
        const respuesta = await fetch('/api/ranking/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (respuesta.ok) {
            const topGatos = await respuesta.json();
            dibujarPodio(topGatos);
        } else {
            contenedor.innerHTML = "<p style='color: #a87b66;'>Hubo un problema al obtener el top felino.</p>";
        }
    } catch (error) {
        console.error("Error de conexión:", error);
        contenedor.innerHTML = "<p style='color: red;'>No se pudo conectar con el servidor de ranking.</p>";
    }
}

function dibujarPodio(listaDeGatos) {
    const contenedor = document.getElementById('podio-ganadores');
    contenedor.innerHTML = "";

    if (listaDeGatos.length === 0) {
        contenedor.innerHTML = "<p>¡Aún no hay suficientes votos para armar el podio! </p>";
        return;
    }

    const medallas = ["🥇", "🥈", "🥉"];

    listaDeGatos.forEach((gato, indice) => {
        const itemHTML = `
            <div class="podio-item puesto-${indice + 1}">
                <div class="medalla">${medallas[indice] || "⋆"}</div>
                <div class="podio-info">
                    <h4>${gato.cat || "Gatito Anónimo"}</h4>
                    <p>${gato.caption ? gato.caption.substring(0, 50) + "..." : "Sin descripción"}</p>
                </div>
                <div class="podio-likes">♡ ${gato.likes}</div>
            </div>
        `;
        contenedor.innerHTML += itemHTML;
    });
}
