const emailInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');
const loginBtn = document.getElementById('login-btn');

loginBtn.addEventListener('click', async () => {
    
    const datosUsuario = {
        email: emailInput.value, 
        password: passwordInput.value 
    };

    try {
        const respuesta = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosUsuario) 
        });

        if (respuesta.ok) {
            const resultado = await respuesta.json();
            console.log("¡Login exitoso, miau!", resultado);
            alert("¡Bienvenido a Kittys.com!");
        } else {
            console.error("Credenciales incorrectas");
            alert("Error: Revisa tu correo o contraseña.");
        }

    } catch (error) {
        console.error("Error al conectar con el servidor:", error);
        alert("El servidor de los gatitos está durmiendo; intenta más tarde.");
    }
});
