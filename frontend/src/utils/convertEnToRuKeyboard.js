const ruKeyboard = "йцукенгшщзхъфывапролджэячсмитьбю";
const enKeyboard = "qwertyuiop[]asdfghjkl;'zxcvbnm,.";
export const convertEnToRuKeyboard = (text) => {
    return [...text]
        .map((ch) => {
            const foundEnCharIdx = enKeyboard.indexOf(ch.toLowerCase());
            const ruChar = foundEnCharIdx === -1 ? ch : ruKeyboard[foundEnCharIdx];

            const isLowerCase = ch === ch.toLowerCase();
            return isLowerCase ? ruChar : ruChar.toUpperCase();
        })
        .join("");
};
