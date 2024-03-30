import React, { useState, useEffect } from 'react';
import './CustomDesignPrinters.css';
import { useParams } from 'react-router-dom';
import PageTitle from '../PageTitle/PageTitle';

const backend = import.meta.env.VITE_APP_BACKEND;

const CustomDesignPrinters = () => {
    const { id } = useParams();
    const [data, setData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${backend}/designs/details-to-printer/${id}`, {
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    },
                });
                console.log(response.status);
                if (response.ok) {
                    const datos = await response.json();
                    setData(datos);
                } else if (response.status === 403) {
                    alert('No tienes permiso para acceder a esta página. Solo los impresores pueden ver los detalles.');
                    window.location.href = '/';
                } else if (response.status === 401) {
                    alert('No estás logueado. Por favor, inicia sesión.');
                    window.location.href = '/login';
                } else {
                    alert('Error al cargar los detalles del diseño.');
                    window.location.href = '/';
                }
            } catch (error) {
                console.log(error);
                alert('Error al cargar los detalles del diseño.');
            }
        };

        fetchData();
    }, [id]);

    const handlePrint = async () => {
        try {
            
            const response = await fetch(`${backend}/designs/update-status/${id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                },
            });
            const result = await response.json();
            if (result.status === 'success') {
                alert('Asignación realizada. Ya puede empezar a imprimir la pieza');
                window.location.href = '/';
            } else {
                alert('Error al actualizar el diseño.');
            }
        } catch (error) {
            console.error('Error al actualizar el diseño:', error);
        }
    };

    return (
        <>
            <PageTitle title="Detalles de la solicitud" />
            <div className="custom-design-printers">
                <h2>{data && data.name}</h2>
                <p>Volumen: {data && data.volume} cm³</p>
                <p>Área: {data && data.area} cm²</p>
                <p>Dimensiones: {data && `${data.dimensions.width} x ${data.dimensions.height} x ${data.dimensions.depth} cm`}</p>
                <p>Peso: {data && data.weight} kg</p>
                <p>Calidad: {data && data.quality}</p>
                <p>Color: {data && data.color}</p>
                <p>Cantidad: {data && data.quantity}</p>
                <p>Precio: {data && data.price}€</p>
                <button onClick={handlePrint}>Imprimir</button>
            </div>
        </>
    );
};

export default CustomDesignPrinters;
