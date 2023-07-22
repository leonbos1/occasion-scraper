function fixBase64Image(cars) {
    cars.value.forEach(car => {
        if (!car.base_image.startsWith('data:image')) {
            console.log('fixing base64 image');
            car.base_image = 'data:image/png;base64,' + car.base_image;
        }
    });
}

export default fixBase64Image;