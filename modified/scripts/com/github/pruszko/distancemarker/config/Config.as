package com.github.pruszko.distancemarker.config
{
   import com.github.pruszko.distancemarker.utils.Disposable;
   
   public class Config implements Disposable
   {
      
      private var _decimalPrecision:int = 0;
      
      private var _textSize:int = 11;
      
      private var _textColor:int = 16777215;
      
      private var _textAlpha:Number = 1;
      
      private var _drawTextOutline:Boolean = true;
      
      private var _drawTextShadow:Boolean = true;
      
      private var _drawDistanceUnit:Boolean = true;
      
      private var _nearDistanceColor:int = 39423;
      
      private var _zone3DistanceColor:int = 16711936;
      
      private var _zone4DistanceColor:int = 16711936;
      
      private var _zone5DistanceColor:int = 16711936;
      
      private var _farDistanceColor:int = 16770304;
      
       private var _impreciseDisplayMode:String = "except-view-range";
      
       private var _sizeBonusZone1:int = 7;
      
        private var _sizeBonusZone2:int = 5;
      
        private var _sizeBonusZone3:int = 4;
      
        private var _sizeBonusZone4:int = 3;
      
        private var _sizeBonusZone5:int = 2;

       private var _sizeBonusZone6:int = 0;
      
      public function Config()
      {
         super();
      }
      
      public function deserialize(param1:Object) : void
      {
         this._decimalPrecision = param1["decimal-precision"];
         this._textSize = param1["text-size"];
         this._textColor = param1["text-color"];
         this._textAlpha = param1["text-alpha"];
         this._drawTextOutline = param1["draw-text-outline"];
         this._drawTextShadow = param1["draw-text-shadow"];
         this._drawDistanceUnit = param1["draw-distance-unit"];
         this._nearDistanceColor = param1["near-distance-color"];
         this._zone3DistanceColor = param1["zone3-distance-color"];
         this._zone4DistanceColor = param1["zone4-distance-color"];
         this._zone5DistanceColor = param1["zone5-distance-color"];
         this._farDistanceColor = param1["far-distance-color"];
          this._impreciseDisplayMode = param1["imprecise-display-mode"];
         this._sizeBonusZone1 = param1["size-bonus-zone1"];
         this._sizeBonusZone2 = param1["size-bonus-zone2"];
         this._sizeBonusZone3 = param1["size-bonus-zone3"];
         this._sizeBonusZone4 = param1["size-bonus-zone4"];
          this._sizeBonusZone5 = param1["size-bonus-zone5"];
          this._sizeBonusZone6 = param1["size-bonus-zone6"];
      }
      
      public function disposeState() : void
      {
      }
      
      public function get decimalPrecision() : int
      {
         return this._decimalPrecision;
      }
      
      public function get textSize() : int
      {
         return this._textSize;
      }
      
      public function get textColor() : int
      {
         return this._textColor;
      }
      
      public function get textAlpha() : Number
      {
         return this._textAlpha;
      }
      
      public function get drawTextOutline() : Boolean
      {
         return this._drawTextOutline;
      }
      
      public function get drawTextShadow() : Boolean
      {
         return this._drawTextShadow;
      }
      
      public function get drawDistanceUnit() : Boolean
      {
         return this._drawDistanceUnit;
      }
      
      public function get nearDistanceColor() : int
      {
         return this._nearDistanceColor;
      }
      
      public function get zone3DistanceColor() : int
      {
         return this._zone3DistanceColor;
      }
      
      public function get zone4DistanceColor() : int
      {
         return this._zone4DistanceColor;
      }
      
      public function get zone5DistanceColor() : int
      {
         return this._zone5DistanceColor;
      }
      
      public function get farDistanceColor() : int
      {
         return this._farDistanceColor;
      }
      
       public function get impreciseDisplayMode() : String
       {
          return this._impreciseDisplayMode;
       }
      
      public function get sizeBonusZone1() : int
      {
         return this._sizeBonusZone1;
      }
      
      public function get sizeBonusZone2() : int
      {
         return this._sizeBonusZone2;
      }
      
      public function get sizeBonusZone3() : int
      {
         return this._sizeBonusZone3;
      }
      
      public function get sizeBonusZone4() : int
      {
         return this._sizeBonusZone4;
      }
      
       public function get sizeBonusZone5() : int
      {
          return this._sizeBonusZone5;
       }

       public function get sizeBonusZone6() : int
       {
          return this._sizeBonusZone6;
       }
   }
}
