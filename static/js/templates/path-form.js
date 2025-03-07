export default `
<div>
    <div v-for="field in pathFields" :key="field.name">
        <form-group 
            :label="field.label"
            v-model="formData[field.name]"
            :placeholder="CONFIG[field.placeholderKey] || ''"
            :input-id="field.name"
            :dual="!!field.secondary"
            :secondary-placeholder="field.secondary ? CONFIG[field.secondary.placeholderKey] || '' : ''"
            :secondary-value="field.secondary ? formData[field.secondary.name] : ''"
            :secondary-id="field.secondary ? field.secondary.name : ''"
            :secondary-disabled="field.secondary && field.secondary.disabled"
            :amplicon-info-value="formData.ampliconInfo"
            @secondary-input="field.secondary ? formData[field.secondary.name] = $event : null"
            :custom-class="field.customClass"
            :info-text="field.infoText">
        </form-group>
    </div>
</div>

`;