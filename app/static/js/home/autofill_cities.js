 let autocomplete;
      let citiesFiled;

      function initAutocomplete() {
        citiesFiled = document.querySelector("#city-input");

        // Create the autocomplete object, restricting the search predictions to
        // addresses in the US and Canada.
        autocomplete = new google.maps.places.Autocomplete(citiesFiled, {
          componentRestrictions: { country: ["us", "ca"] },
          types: ["(cities)"],
        });
        citiesFiled.focus();
        // When the user selects an address from the drop-down, populate the
        // address fields in the form.
        autocomplete.addListener("place_changed", fillInAddress);
      }

      function fillInAddress() {
        // Get the place details from the autocomplete object.
        const place = autocomplete.getPlace();
        let address1 = "";
        let postcode = "";

        // Get each component of the address from the place details,
        // and then fill-in the corresponding field on the form.
        // place.address_components are google.maps.GeocoderAddressComponent objects
        // which are documented at http://goo.gle/3l5i5Mr
        for (const component of place.address_components) {
          const componentType = component.types[0];

          console.log(componentType);
          console.log(component.long_name);
          console.log("\n");
          switch (componentType) {


            case "locality":
              citiesFiled.value = component.long_name;
              break;

            case "country":
              document.querySelector("#country").value = component.long_name;
              break;
          }
        }
        citiesFiled.value = address1;
        // After filling the form with address components from the Autocomplete
        // prediction, set cursor focus on the second address line to encourage
        // entry of subpremise information such as apartment, unit, or floor number.
      }