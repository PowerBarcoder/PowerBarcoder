export default `
<div class="border border-gray p-3 bg-light mt-3">
    <h5>Locus {{ index + 1 }}</h5>
    <div v-for="field in locusFields" :key="field.name">
        <form-group
            :label="field.label + ' ' + (index + 1)"
            v-model="formData[field.name][index]"
            :placeholder="getPlaceholder(field.placeholderKey)"
            :input-id="field.name + (index > 0 ? index + 1 : '')"
            :input-class="field.inputClass"
            :tooltip-id="'tooltip1-' + field.name + (index > 0 ? '_' + index : '')"
            :dual="!!field.secondary"
            :secondary-placeholder="field.secondary ? CONFIG[field.secondary.placeholderKey] : null"
            :secondary-value="field.secondary ? formData[field.secondary.name][index] : null"
            :secondary-id="field.secondary ? field.secondary.name + (index > 0 ? index + 1 : '') : null"
            :secondary-disabled="field.secondary && field.secondary.disabled"
            :amplicon-info-value="formData.ampliconInfo"
            @secondary-input="field.secondary ? formData[field.secondary.name].splice(index, 1, $event) : null"
            :custom-class="field.customClass"
            :info-text="field.infoText">
        </form-group>
    </div>
    <div class="d-flex align-items-center">
        <button :id="'autoCompleteWithRBCL' + index" class="btn btn-warning" type="button" @click="fillWithRBCL">
            Demo rbcL
        </button>
        &nbsp;
        <button :id="'autoCompleteWithTRNLF' + index" class="btn btn-warning" type="button" @click="fillWithTRNLF">
            Demo trnLF
        </button>
    </div>
</div>

`;