/**
 * @deprecated 
 */
function fixBase64Image(cars) {
    cars.value.forEach(car => {
        if (!car.base_image.startsWith('data:image')) {
            car.base_image = 'data:image/png;base64,' + car.base_image;
        }
    });
}

export default fixBase64Image;